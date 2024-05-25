from django.urls import reverse_lazy

JAZZMIN_SETTINGS = {
    "site_title": "UNCLE MAO",
    "site_header": "UNCLE MAO",
    "site_brand": "UNCLE MAO",
    "site_logo": "logo.jpeg",
    "login_logo": None,
    "login_logo_dark": None,
    "site_logo_classes": "img-circle",
    "site_icon": "logo.jpeg",
    "welcome_sign": "Welcome to the UNCLE MAO admin",
    "copyright": "UNCLE MAO Ltd",
    "search_model": ["client.FulFillmentRequest", "client.LogisticRequest"],
    "user_avatar": None,
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Support", "url": "https://t.me/usmnvk", "new_window": True},
        {"app": "auth"},
        {"app": "fulfillment", "name": "My Fulfillment", "icon": "fas fa-truck-loading"},
    ],
    "usermenu_links": [
        {"name": "Support", "link": "admin:support", "icon": "fas fa-life-ring"},
        {"model": "auth.user"},
    ],
    "show_sidebar": True,
    "navigation_expanded": False,
    "hide_apps": [],
    "hide_models": ["fulfillment.TagingPriceRange"],
    "order_with_respect_to": ["auth", "fulfillment", "client", "stock"],
    "custom_links": {
        "fulfillment.MarkingType": [
            {
                "name": "Manage Marking Types",
                "link": "admin:fulfillment_markingtype_changelist",
                "permissions": ["fulfillment.view_markingtype", "fulfillment.change_markingtype"],
            }
        ],
        "fulfillment.CargoType": [
            {
                "name": "Manage Cargo Types",
                "link": "admin:fulfillment_cargotype_changelist",
                "permissions": ["fulfillment.view_cargotype", "fulfillment.change_cargotype"],
            }
        ],
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
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
    "language_chooser": False,
}

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
}
