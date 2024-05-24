from django.urls import reverse_lazy

JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "UNCLE MAO",
    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "UNCLE MAO",
    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "UNCLE MAO",
    # Logo to use for your site, must be present in static files, used for brand on top left
    "site_logo": "books/img/logo.png",
    # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
    "login_logo": None,
    # Logo to use for login form in dark themes (defaults to login_logo)
    "login_logo_dark": None,
    # CSS classes that are applied to the logo above
    "site_logo_classes": "img-circle",
    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": None,
    # Welcome text on the login screen
    "welcome_sign": "Welcome to the UNCLE MAO admin",
    # Copyright on the footer
    "copyright": "UNCLE MAO Ltd",
    "search_model": ["client.FulFillmentRequest", "client.LogisticRequest"],
    "user_avatar": None,
    ############
    # Top Menu #
    ############
    # Links to put along the top menu
    "topmenu_links": [
        # Url that gets reversed (Permissions can be added)
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        # external url that opens in a new window (Permissions can be added)
        {"name": "Support", "url": "https://t.me/usmnvk", "new_window": True},
        # model admin to link to (Permissions checked against model)
        {"model": "auth.User"},
        # App with dropdown menu to all its models pages (Permissions checked against models)
    ],
    #############
    # User Menu #
    #############
    #############
    # Side Menu #
    #############
    # Whether to display the side menu
    "show_sidebar": True,
    # Whether to aut expand the menu
    "navigation_expanded": False,
    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": [],
    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": ["fulfillment.TagingPriceRange"],
    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    # Configure app order in the sidebar
    "order_with_respect_to": ["client", "fulfillment"],
    "custom_links": {
        "fulfillment.MarkingType": [
            {
                "name": "Manage Marking Types",
                "link": "admin:fulfillment_markingtype_changelist",
                "permissions": [
                    "fulfillment.view_markingtype",
                    "fulfillment.change_markingtype",
                ],
            }
        ],
        "fulfillment.CargoType": [
            {
                "name": "Manage Cargo Types",
                "link": "admin:fulfillment_cargotype_changelist",
                "permissions": [
                    "fulfillment.view_cargotype",
                    "fulfillment.change_cargotype",
                ],
            }
        ],
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    # Sidebar Menu Structure
    "usermenu_links": [
        {"name": "Support", "link": "admin:support", "icon": "fas fa-life-ring"},
        {"model": "auth.user"},
    ],
    "topmenu_links": [
        {"app": "auth"},
        {
            "app": "fulfillment",
            "name": "My Fulfillment",
            "icon": "fas fa-truck-loading",
        },
    ],
    # Configuration of apps and models on the sidebar
    "order_with_respect_to": ["auth", "fulfillment", "client", "stock"],
    "models": {
        "client.ClientModel": {"icon": "fas fa-user", "order": 1},
        "fulfillment.CargoServiceType": {"icon": "fas fa-truck-moving", "order": 1},
        "fulfillment.CargoType": {"icon": "fas fa-boxes", "order": 2},
        "fulfillment.MarkingType": {"icon": "fas fa-tags", "order": 3},
        "stock.StockModel": {"icon": "fas fa-warehouse", "order": 1},
    },
    "custom_groups": {
        "Client": {
            "models": ["client.TelegramClient"],
            "icon": "fas fa-user",
            "order": 1,
        },
        "Fulfillment": {
            "models": [
                "fulfillment.CargoServiceType",
                "fulfillment.CargoType",
                "fulfillment.MarkingType",
            ],
            "icon": "fas fa-truck-loading",
            "order": 2,
        },
        "Stock": {
            "models": ["stock.StockModel"],
            "icon": "fas fa-warehouse",
            "order": 3,
        },
    },
    "changeform_format": "collapsible",
    # Add a language dropdown into the admin
    "language_chooser": False,
}

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
}
