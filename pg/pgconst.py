skipPokemons = False #to indicate if we should try to catch them

MIN_RECOGNITION_VAL = 0.01 #if we get below that value indicates that we found template

DEL_ITEMS_POKEYBALL=1
DEL_ITEMS_RAZZ_BERRY=2
DEL_ITEMS_NANAB_BERRY=4
DEL_ITEMS_POTION=8
DEL_ITEMS_REVIVE=16


SCREEN_MAIN_MAP = 1
SCREEN_MAIN_MENU = 2
SCREEN_INSIDE_POKESTOP = 3
SCREEN_INSIDE_GYM = 4
SCREEN_HAS_EXIT_BUTTON = 5
SCREEN_CATCHING_POKEMON = 6
SCREEN_CAUGTH_POKEMON_POPUP = 7
SCREEN_POKEMON_STATS_POPUP = 8
SCREEN_GYM_TOO_FAR = 9
SCREEN_PASSENGER = 10
SCREEN_SHOP = 11
SCREEN_HAS_GYM_JOIN = 12
SCREEN_POKEMONS_SELECTION = 13
SCREEN_GYM_CONFIRM_BUTTON = 14
SCREEN_ANDROID_HOME = 15

MESSAGE_ANDROID_TYPE_TEST = 1
MESSAGE_ANDROID_SCREEN_CAP = 2
MESSAGE_ANDROID_SEND_TOUCH = 3
MESSAGE_ANDROID_SEND_SWIPE = 4

ANDROID_CLIENT_RECV_TIMEOUT = 3

COORDS_CENTER = "coord_center"
COORDS_MAIN_MENU_BUTTON = "coord_main_menu_button"
COORDS_EXIT_BUTTON = "coord_close_poke_stop"
COORDS_ITEMS_BUTTON = "coord_items_button"
COORDS_DELETE_ITEM = "coord_delete_item"
COORDS_DISCARD_PLUS_BUTTON = "coord_discard_plus_button"
COORDS_DISCARD_YES_BUTTON = "coord_discard_yes_button"
COORDS_CLOSE_ITEMS_MENU_BUTTON = "coord_close_items_menu_button"
COORDS_LEAVE_CATCH_POKEMON_BUTTON = "coord_leave_catch_pokemon_button"
COORDS_TOP_CP_POKEMON = "coord_top_cp_pokemon"
COORDS_ANDROID_EXIT_BUTTON = "coord_android_exit_button"

SCRIPT_SWIPE_POKESTOP = "script_swipe_pokestop"
SCRIPT_THROW_BALL_NORMAL = "script_throw_ball_normal"
SCRIPT_THROW_BALL_LONG = "script_throw_ball_long"
SCRIPT_THROW_BALL_SHORT = "script_throw_ball_short"
SCRIPT_SCROLL_ITEMS = "script_scrool_items"
SCRIPT_ZOOM_OUT = "script_zoom_out"

TEMPLATE_POKEYDEX_BUTTON_MENU = "template_pokeydex_button_menu"
TEMPLATE_POKEYBALL_MAP_SCREEN = "template_pokeyball_map_screen"

TEMPLATE_POKEY_STOP_DAY = "template_pokey_stop_day"
TEMPLATE_POKEY_STOP_DAY_VISITED = "template_pokey_stop_day_visited"
TEMPLATE_POKEY_STOP_NIGHT = "template_pokey_stop_night"
TEMPLATE_POKEY_STOP_NIGHT_VISITED = "template_pokey_stop_night_visited"

TEMPLATE_EXIT_BUTTON = "template_exit_button"
TEMPLATE_POKE_BALL_DELETE = "template_poke_ball_delete"
TEMPLATE_RAZZ_BERRY_DELETE = "template_razz_berry_delete"
TEMPLATE_NANAB_BERRY_DELETE = "template_nanab_berry_delete"
TEMPLATE_POTION_DELETE = "template_potion_delete"
TEMPLATE_REVIVE_DELETE= "template_revive_delete"

TEMPLATE_CATCH_POKEMON_OK_BUTTON = "template_catch_pokemon_OK_button"
TEMPLATE_CATCH_POKEMON_STATS_SCREEN = "template_catch_pokemon_stats_screen"
TEMPLATE_GYM_MAIN_SCREEN = "template_gym_main_screen"
TEMPLATE_CATCH_POKEMON_SCREEN_DAY = "template_catch_pokemon_screen_day"
TEMPLATE_CATCH_POKEMON_SCREEN_NIGHT = "template_catch_pokemon_screen_night"
TEMPLATE_GYM_TOO_FAR = "template_gym_too_far"
TEMPLATE_PASSENGER = "template_passenger"
TEMPLATE_EXIT_BUTTON_SHOP = "template_exit_button_shop"
TEMPLATE_GYM_JOIN_BUTTON = "template_gym_join_button"
TEMPLATE_POKEMONS_SELECTION = "template_pokemons_selection"
TEMPLATE_CONFIRM_GYM_YES_BUTTON = "template_confirm_gym_yes_button"
TEMPLATE_EXIT_YES_BUTTON = "template_exit_yes_button"

TEMPLATE_ANDROID_PHONE_ICON = "template_android_phone_icon"
TEMPLATE_ANDROID_PG_ICON = "template_android_pg_icon"