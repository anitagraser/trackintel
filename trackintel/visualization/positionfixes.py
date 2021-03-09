import matplotlib.pyplot as plt
import warnings
from trackintel.visualization.osm import plot_osm_streets
from trackintel.visualization.util import regular_figure, save_fig


def plot_positionfixes(positionfixes, out_filename=None, plot_osm=False, axis=None):
    """Plots positionfixes (optionally to a file). If you specify ``plot_osm=True``
    this will use ``osmnx`` to plot streets below the positionfixes. Depending on
    the extent of your data, this might take a long time. The data gets
    transformed to wgs84 for the plotting.

    Parameters
    ----------
    positionfixes : GeoDataFrame
        The positionfixes to plot.

    out_filename : str, optional
        The file to plot to, if this is not set, the plot will simply be shown.

    plot_osm : bool, default False
        If this is set to True, it will download an OSM street network and plot 
        below the staypoints.

    axis : matplotlib.pyplot.Artist, optional
        axis on which to draw the plot

    Examples
    --------
    >>> df.as_positionfixes.plot('output.png', plot_osm=True)
    """
    if axis is None:
        _, ax = regular_figure()
    else:
        ax = axis

    crs_wgs84 = 'EPSG:4326'
    if positionfixes.crs is None:
        warnings.warn("Coordinate System (CRS) is not set, default to WGS84.")
        positionfixes.crs = crs_wgs84
    elif positionfixes.crs != crs_wgs84:
        positionfixes = positionfixes.to_crs(crs_wgs84)

    if plot_osm:
        west = positionfixes.geometry.x.min()
        east = positionfixes.geometry.x.max()
        north = positionfixes.geometry.y.max()
        south = positionfixes.geometry.y.min()
        plot_osm_streets(north, south, east, west, ax)

    positionfixes.plot(ax=ax, markersize=0.5, zorder=2)

    if out_filename is not None:
        save_fig(out_filename, formats=['png'])
    elif axis is None:
        plt.show()
