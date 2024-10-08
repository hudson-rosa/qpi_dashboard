import base64
import dash
from dash import dcc, callback, html
from dash.dependencies import Input, Output

from src.utils.assets_handler import AssetsHandler
from src.models.entity.pie_chart import PieChart
from src.models.entity.bar_chart import BarChart
from src.models.entity.line_chart import LineChart
from src.models.entity.pyramid_chart import PyramidChart

from src.models.mapper.data_mapper import DataMapper
from src.models.mapper.filtering_mapper import FilteringMapper
import src.controllers.app_path_config as app_path_config


data_path = app_path_config.get_data_storage_path()
data_mapper_instance = DataMapper(filename=data_path)
decoded_logo_img = AssetsHandler(
    app_path_config.get_assets_image_logo()
).decode_base64()


def update_figures():
    chart_args_test_names_and_times = [
        ("data_frame", FilteringMapper.filter_test_names_and_times_dictionary()),
        ("template", "plotly_dark"),
    ]
    chart_args_test_levels_and_approaches = [
        ("data_frame", FilteringMapper.filter_test_level_and_approaches()),
        ("template", "plotly_dark"),
    ]
    chart_args_test_suites = [
        ("data_frame", FilteringMapper.filter_test_suites()),
        ("template", "plotly_dark"),
    ]

    chart_args_test_segregated_levels_and_approaches = [
        (
            "data_frame_group_a",
            FilteringMapper.filter_test_level_and_approaches_by(
                filter_by_key="test_approach", filter_by_value="automated"
            ),
        ),
        (
            "data_frame_group_b",
            FilteringMapper.filter_test_level_and_approaches_by(
                filter_by_key="test_approach", filter_by_value="manual"
            ),
        ),
        ("template", "plotly_dark"),
    ]

    pie_fig_1 = PieChart(**dict(chart_args_test_levels_and_approaches))
    pie_fig_2 = PieChart(**dict(chart_args_test_suites))
    bar_fig_1 = BarChart(**dict(chart_args_test_names_and_times))
    line_fig = LineChart(**dict(chart_args_test_names_and_times))
    pyramid_fig = PyramidChart(
        **dict(chart_args_test_segregated_levels_and_approaches)
    )
    bar_fig_2 = BarChart(**dict(chart_args_test_suites))

    print("\n------->>> RAW DATA: \n", data_mapper_instance.get_composed_data_frame())

    return pie_fig_1, pie_fig_2, bar_fig_1, bar_fig_2, line_fig, pyramid_fig


def render_layout():
    pie_fig_1, pie_fig_2, bar_fig_1, bar_fig_2, line_fig, pyramid_fig = update_figures()

    plot_pie_chart_auto_and_manual_cov = dcc.Graph(
        id="pie-chart",
        figure=pie_fig_1.create(
            slice_values="count",
            names="test_approach",
            title="Test Coverage: Automated Vs. Manual",
            slice_colors=["seagreen", "orange"],
        ),
    )

    plot_pie_chart_suite_cov = dcc.Graph(
        id="pie-chart",
        figure=pie_fig_2.create(
            slice_values="count", names="test_suites", title="Test Coverage per Suite"
        ),
    )

    plot_pyramid_chart = dcc.Graph(
        id="pyramid-chart",
        figure=pyramid_fig.create(
            x_group_a_axis="count",
            y_group_a_axis="test_level",
            x_group_b_axis="count",
            y_group_b_axis="test_level",
            title_x="Total tests",
            title_y="Test level",
            legend_group_a_axis="Automated",
            legend_group_b_axis="Manual",
            title="Test Pyramid Coverage (per level)",
        ),
    )

    plot_line_chart_effort = dcc.Graph(
        id="line-chart",
        figure=line_fig.create(
            x_axis="test_name",
            y_axis="total_time",
            title="Test Effort Distribution (in seconds)",
        ),
    )

    plot_bar_chart_total_tests = dcc.Graph(
        id="bar-chart",
        figure=bar_fig_2.create(
            x_axis="test_suites",
            y_axis="count",
            title="Total Tests per Suite",
        ),
    )

    dashboard_layout = html.Div(
        [
            html.Img(
                src=decoded_logo_img,
                className="qpi_logo",
            ),
            html.H1("Analytics"),
            html.Div(
                className="tabs",
                children=[
                    dcc.Link(
                        "View Analytics Dashboard",
                        href="/dashboard",
                        className="tab--selected",
                    ),
                    dcc.Link(
                        "Register Test Efforts",
                        href="/register_tests",
                        className="tab--unselected",
                    ),
                    dcc.Link(
                        "Register Project",
                        href="/register_project",
                        className="tab--unselected",
                    ),
                ],
            ),
            html.Div(
                className="content-frame",
                children=[
                    html.H2(
                        children="Test Distribution & Coverage",
                        className="header-card",
                    ),
                    html.Div(
                        className="row",
                        children=[
                            html.Div(
                                children=plot_pie_chart_auto_and_manual_cov,
                                id="pie-chart-container",
                                className="chart-card-flex",
                            ),
                            html.Div(
                                children=plot_pie_chart_suite_cov,
                                id="pie-chart-container",
                                className="chart-card-flex",
                            ),
                        ],
                    ),
                    html.Div(
                        children=plot_pyramid_chart,
                        id="pyramid-chart-container",
                        className="chart-card",
                    ),
                    html.Div(
                        children=plot_line_chart_effort,
                        id="line-chart-container",
                        className="chart-card",
                    ),
                    html.Div(
                        children=plot_bar_chart_total_tests,
                        id="bar-chart-container",
                        className="chart-card",
                    ),
                ],
            ),
        ]
    )

    return dashboard_layout
