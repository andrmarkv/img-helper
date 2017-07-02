from pg import pgconst, pgutil
from time import sleep


"""
Clear bag main function. It has to start from the main screen (map).
Parameters:
    items - mask of the items that needs to be deleted, see DEL_ITEMS_*
    ps - phone specific settings
    clientAndroid - client to handle Android requests
"""
def clear_bag(clientAndroid, items, ps):
    print "started clear_bag process, item categories to delete: " + str(items)
    #Check if we are on the main screen
    img = clientAndroid.get_screen_as_array()
                    
    if img is None:
        print "clear_bag Error! Can't capture the screen."
        return
    
    if not pgutil.is_main_map(img, ps)[0]:
        print "clear_bag Error! wrong start screen."
        pgutil.save_array_as_png(img, "/tmp/", "wrong_main_screen")
        return
    
    clientAndroid.send_touch(ps.getCoord(pgconst.COORDS_MAIN_MENU_BUTTON))
    clientAndroid.send_touch(ps.getCoord(pgconst.COORDS_ITEMS_BUTTON))
    
    print "Checking items..."
    
    #check items in the loop using scroll
    for i in range(0,8):
        #should be initial items list screen
        img = clientAndroid.get_screen_as_array()    
        
        resutls = pgutil.is_items_visible(img, items, ps)
        if resutls is not None:
            for r in resutls:
                #Remove detected item from the list of items
                items = items & (~r[0])
                
                #Click delete button for the given item, r[1][2][1] should give y of the center of the match region
                (x, y) = ps.getCoord(pgconst.COORDS_DELETE_ITEM)
                clientAndroid.send_touch((x, r[1][2][1]))
                
                #Click select how many items 
                for j in range (0, 1):
                    clientAndroid.send_touch(ps.getCoord(pgconst.COORDS_DISCARD_PLUS_BUTTON))
                
                #this is coordinates of yes button
                clientAndroid.send_touch(ps.getCoord(pgconst.COORDS_DISCARD_YES_BUTTON))
                
                print "deleted item: " + str(r[0])
        
        #Exit if we already processed all selected items
        if items <= 0 :
            sleep(2)
            break
        
        #Scroll
        clientAndroid.send_swipe(ps.getScript(pgconst.SCRIPT_SCROLL_ITEMS))
        sleep(1)
        
    #Exiting Items menu
    #this is coordinates of yes button
    clientAndroid.send_touch(ps.getCoord(pgconst.COORDS_CLOSE_ITEMS_MENU_BUTTON))

    
    print "Finished clearing bag"
    
    return

def click_sector(clientAndroid, center, r0, r1, a0, a1):
    #get dots within specified sector
    dots = pgutil.get_sector_dots(center, r0, r1, a0, a1)
    
    #click selected dots, do not sleep after each click
    for dot in dots:
        clientAndroid.send_touch((dot[0], dot[1]), 0)
        
    print "Finished clicking sector"
                        
"""
Perform action based on what scren we are on
Parameters:
    clientAndroid - client to handle Android requests
    ps - phone specific settings
Supported actions:
    - check pokestop
    TODO: - catch pokemon
    TODO: - close wrong window?
Returns:
    - 1 in case screen was identified and some action was performed
    - 0 in case it was not able to identify screen and perform action
"""
def do_relevant_action(clientAndroid, ps):
    #get screen
    img = clientAndroid.get_screen_as_array()
    
    #identify screen
    result = pgutil.identify_screen(img, ps)
    
    #do actions based on the screen
    if result is None:
        #some mitigations for unknown screns
        sleep(1)
        img = clientAndroid.get_screen_as_array()
        result = pgutil.identify_screen(img, ps)
        
        if result is None:
            clientAndroid.send_touch(ps.getCoord(pgconst.COORDS_EXIT_BUTTON))
            #we got unknown screen, save it
            pgutil.save_array_as_png(img, "/tmp", "unknown_screen")
            return 0 
    
    res = 0
    
    if result[0] == pgconst.SCREEN_INSIDE_POKESTOP:
        collect_pokestop(clientAndroid, ps)
        res = 1
    elif result[0] == pgconst.SCREEN_INSIDE_GYM:
        clientAndroid.send_touch(ps.getCoord(pgconst.COORDS_EXIT_BUTTON))
        res = 1
    elif result[0] == pgconst.SCREEN_CATCHING_POKEMON:
        catch_pokemon(clientAndroid, ps)
        res = 1
    elif result[0] == pgconst.SCREEN_HAS_EXIT_BUTTON:
        clientAndroid.send_touch(ps.getCoord(pgconst.COORDS_EXIT_BUTTON))
        res = 1
    elif result[0] == pgconst.SCREEN_MAIN_MAP:
        #do nothing as it is required screen
        print "Main screen"
        res = 1
    elif result[0] == pgconst.SCREEN_POKEMON_STATS_POPUP:
        clientAndroid.send_touch(ps.getCoord(pgconst.COORDS_EXIT_BUTTON))
        res = 1
    
    if res == 0:
        print "was not able to perform proper action "
        pgutil.save_array_as_png(img, "/tmp", "unknown_acions")
    
    return res
 
 
def catch_pokemon(clientAndroid, ps):
    print "Processing catch pokemon"
    
    i = 0
    while (i < 10):
        
        #Throw ball
        if i == 3 or i == 6:
            clientAndroid.send_swipe(ps.getScript(pgconst.SCRIPT_THROW_BALL_LONG))
        elif i == 4 or i == 8:
            clientAndroid.send_swipe(ps.getScript(pgconst.SCRIPT_THROW_BALL_SHORT))
        else:
            clientAndroid.send_swipe(ps.getScript(pgconst.SCRIPT_THROW_BALL_NORMAL))
        
        i = i + 1
            
        #First attempt to identify catch pokemon screen
        result = pgutil.identify_catch_screen(clientAndroid, ps)
        
        if result is not None:
            if result[0] == pgconst.SCREEN_CAUGTH_POKEMON_POPUP:
                res = exit_from_catch_ok(clientAndroid, ps, result)
                #1 indicates that we caught pokemon and exited popups
                if (res == 1):
                    print "Caught pokemon on attempt: %d" % i  
                    return 1
            elif result[0] == pgconst.SCREEN_POKEMON_STATS_POPUP:
                clientAndroid.send_touch(ps.getCoord(pgconst.COORDS_EXIT_BUTTON))
                print "Got to pokemon stats on attempt: %d" % i
                return 1
            elif result[0] == pgconst.SCREEN_CATCHING_POKEMON:
                print "Did not catch pokemon on attempt: %d, continuing..." % i
                continue
            elif result[0] == pgconst.SCREEN_MAIN_MAP:
                #pokemon run away
                print "Pokemon run away after attemps %d!" % i
                return 1
            elif result[0] == pgconst.SCREEN_HAS_EXIT_BUTTON:
                #that is just in case
                clientAndroid.send_touch(ps.getCoord(pgconst.COORDS_EXIT_BUTTON))
                print "Strange state in the catching pokemon process, exiting catching, attemp: %d!" % i
                return 1
        
        print "Waiting for 3 pokeball shakes (10sec) attempt: %d..." % i
        sleep(10)
        print "Waiting is done"
        
        #After sleep attempt to identify catch pokemon screen
        result = pgutil.identify_catch_screen(clientAndroid, ps)

        if result is not None:    
            if result[0] == pgconst.SCREEN_CAUGTH_POKEMON_POPUP:
                res = exit_from_catch_ok(clientAndroid, ps, result)
                #1 indicates that we caught pokemon and exited popups
                if (res == 1):
                    print "Caught pokemon on attempt: %d" % i  
                    return 1
            elif result[0] == pgconst.SCREEN_POKEMON_STATS_POPUP:
                clientAndroid.send_touch(ps.getCoord(pgconst.COORDS_EXIT_BUTTON))
                print "Got to pokemon stats on attempt: %d" % i
                return 1
            elif result[0] == pgconst.SCREEN_CATCHING_POKEMON:
                print "Did not catch pokemon on attempt: %d, continuing..." % i
            elif result[0] == pgconst.SCREEN_MAIN_MAP:
                #pokemon run away
                print "Pokemon run away after attemps %d!" % i
                return 1
            elif result[0] == pgconst.SCREEN_HAS_EXIT_BUTTON:
                #that is just in case
                clientAndroid.send_touch(ps.getCoord(pgconst.COORDS_EXIT_BUTTON))
                print "Strange state in the catching pokemon process, exiting catching, attemp: %d!" % i
                return 1
    
    print "Was not able to catch pokemon after, attempt: %d, exiting catching" % i
    img = clientAndroid.get_screen_as_array()
    #we got unknown screen, save it
    pgutil.save_array_as_png(img, "/tmp", "missed_catch")
    clientAndroid.send_touch(ps.getCoord(pgconst.COORDS_LEAVE_CATCH_POKEMON_BUTTON))
            
def exit_from_catch_ok(clientAndroid, ps, result):
    #Click OK button for the given item, result[1][2][1] should give y of the center of the match region
    (x, y) = ps.getCoord(pgconst.COORDS_CENTER)
    clientAndroid.send_touch((x, result[1][2][1]), 2)
    
    #exit from stats screen
    clientAndroid.send_touch(ps.getCoord(pgconst.COORDS_EXIT_BUTTON))
    
    #check if we are on a main screen
    img = clientAndroid.get_screen_as_array()
    r = pgutil.is_main_map(img, ps)
    if r[0]:
        return 1
    
    return 0
           
                        
def click_donut(clientAndroid, ps, center, r0, r1, count):
    da = 360/count #this is angle of each sector
    a0 = 0
    for i in range (0, count):
        a1 = a0 + da
        click_sector(clientAndroid, center, r0, r1, a0, a1)
        a0 = a1
        
        #do something useful if possible
        print "Waiting for 1 sec after clicks..."
        sleep(1)
        res = do_relevant_action(clientAndroid, ps)
        
        #check if we were able to detect proper screen and if not retry after timeout
        if res == 0:
            print "Waiting for 3 sec after clicks..."
            sleep(3)
            print "Retrying to identify screen"
            do_relevant_action(clientAndroid, ps)
            
    #click center of the donut as well            
    clientAndroid.send_touch(ps.getCoord(center))
    
    print "Finished clicking donut"
        
def look_around(clientAndroid, ps):
    print "Performing look around"
    
    #some helper variables
    phone_center = ps.getCoord(pgconst.COORDS_CENTER)
    
    r0 = 50
    r1 = int (phone_center[0] * 0.8)
    c = (phone_center[0], int(phone_center[1] * 2 * 0.7))
    
    #click around center performing actions per sector
    click_donut(clientAndroid, ps, c, r0, r1, 12)
    
    print "Look around is finished"
    
    return
        
        
def collect_pokestop(clientAndroid, ps):
    print "Processing pokestop"
    clientAndroid.send_swipe(ps.getScript(pgconst.SCRIPT_SWIPE_POKESTOP))
    sleep(1)
    clientAndroid.send_touch(ps.getCoord(pgconst.COORDS_EXIT_BUTTON))
    
def hexdump(src, length=16):
    result = []
    digits = 4 if isinstance(src, unicode) else 2
    for i in xrange(0, len(src), length):
        s = src[i:i+length]
        hexa = b' '.join(["%0*X" % (digits, ord(x))  for x in s])
        text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.'  for x in s])
        result.append( b"%04X   %-*s   %s" % (i, length*(digits + 1), hexa, text) )
        
    tmp = b'\n'.join(result)
    print tmp
    
    return tmp
        
        
        
    