from dash import dcc, html

import src.controllers.app_path_config as app_path_config
from src.views.layout import html_component_header_tabs
from src.utils.assets_handler import AssetsHandler

decoded_logo_img = AssetsHandler(
    app_path_config.get_assets_image_logo()
).decode_base64()


def render_layout():
    return html.Div(
        [
            html_component_header_tabs.render_logo(),
            html_component_header_tabs.render_page_title(current_page_identifier="projects"),
            html_component_header_tabs.render_tabs(active_tab_identifier="projects"),
            html.Div(
                className="form-content",
                children=[
                    html.Ul(
                        html.Li(
                            html.Div(
                                className="section-group",
                                children=[
                                    html.Div(
                                        className="grid-2",
                                        children=[
                                            dcc.Input(
                                                id="rp--project-id",
                                                type="text",
                                                placeholder="Project id",
                                                required=True,
                                                readOnly=True,
                                                className="inline-grid",
                                            ),
                                            html.Button(
                                                "Generate new ID",
                                                id="rp--generate-id-button",
                                                className="inline-grid",
                                            ),
                                        ],
                                    ),
                                    dcc.Input(
                                        id="rp--project-name",
                                        type="text",
                                        placeholder="Enter project name",
                                        required=True,
                                    ),
                                ],
                            )
                        )
                    ),
                    html.Label("Required fields", className="required-msg"),
                    html.Div(id="rp--output-message-projects", className="output-msg"),
                    html.Div(
                        className="grid grid-2",
                        children=[
                            html.Button("Save", id="rp--save-button", n_clicks=0),
                            html.Button("Update", id="rp--update-button", n_clicks=0),
                            html.Div(
                                className="section-group",
                                children=[
                                    html.Div(
                                        id="rp--delete-output-message-projects",
                                        className="output-msg",
                                    ),
                                    dcc.Input(
                                        id="rp--delete-project-id",
                                        type="text",
                                        placeholder="Enter a project ID to delete",
                                    ),
                                    html.Button(
                                        "Delete", id="rp--delete-button", n_clicks=0
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ]
    )
