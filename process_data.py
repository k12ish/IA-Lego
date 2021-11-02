import argparse
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm, colors
from scipy.spatial import Voronoi, voronoi_plot_2d


def process_data(args):
    data = np.load(args.input_path)
    l_r = data['l_r']
    A_p = data['A_p']
    B_p = data['B_p']

    # shape is approx (4000, 2)
    points = np.swapaxes(np.array([A_p, B_p]), 0, 1)
    # add 4 distant dummy points
    points = np.append(
        points, [[999, 999], [-999, 999], [999, -999], [-999, -999]], axis=0
    )

    norm = colors.Normalize(vmin=l_r.min(), vmax=l_r.max(), clip=True)
    mapper = cm.ScalarMappable(norm=norm, cmap=cm.Greys_r)

    vor = Voronoi(points)
    voronoi_plot_2d(vor, show_points=False, show_vertices=False, line_width=0)
    plt.xlim([A_p.min(), A_p.max()])
    plt.ylim([B_p.min(), B_p.max()])
    plt.gca().invert_xaxis()
    plt.gca().invert_yaxis()

    for i in range(len(vor.point_region)):
        region = vor.regions[vor.point_region[i]]
        if not -1 in region:
            polygon = [vor.vertices[j] for j in region]
            plt.fill(*zip(*polygon), color=mapper.to_rgba(l_r[i]))

    if args.output_path:
        plt.axis('off')
        plt.savefig(
            args.output_path,
            bbox_inches='tight',
            transparent=True,
            pad_inches=0
        )
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='produce a high definition image from a .npz file'
    )
    parser.add_argument(
        'input_path', action='store', type=str, help='Input path'
    )
    parser.add_argument(
        'output_path', action='store', nargs='?', type=str, help='Output path.'
    )
    args = parser.parse_args()

    process_data(args)
