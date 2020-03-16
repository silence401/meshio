import xml.etree.ElementTree as ET

import numpy

from .._exceptions import WriteError
from .._helpers import register


def write(filename, mesh):
    if mesh.points.shape[1] == 3 and not numpy.allclose(
        mesh.points[:, 2], 0.0, rtol=0.0, atol=1.0e-14
    ):
        raise WriteError(
            "SVG can only handle flat 2D meshes (shape: {})".format(mesh.points.shape)
        )

    pts = mesh.points[:, :2].copy()
    pts[:, 1] = numpy.max(pts[:, 1]) - pts[:, 1]

    min_x = numpy.min(pts[:, 0])
    min_y = numpy.min(pts[:, 1])
    width = numpy.max(pts[:, 0]) - min_x
    height = numpy.max(pts[:, 1]) - min_y

    svg = ET.Element(
        "svg",
        xmlns="http://www.w3.org/2000/svg",
        version="1.1",
        viewBox="{:.3f} {:.3f} {:.3f} {:.3f}".format(min_x, min_y, width, height),
    )

    style = ET.SubElement(svg, "style")
    opts = ["fill: none", "stroke: black", "stroke-width: 2%", "stroke-linejoin:bevel"]
    style.text = "polygon {" + "; ".join(opts) + "}"

    for cell_block in mesh.cells:
        if cell_block.type not in ["line", "triangle", "quad"]:
            continue
        for cell in cell_block.data:
            ET.SubElement(
                svg,
                "polygon",
                points=" ".join(
                    ["{:.3f},{:.3f}".format(pts[c, 0], pts[c, 1]) for c in cell]
                ),
            )

    tree = ET.ElementTree(svg)
    tree.write(filename)


register("svg", [".svg"], None, {"svg": write})
