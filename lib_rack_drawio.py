import xml.etree.ElementTree as ET
import random
import string
from datetime import datetime, timezone

class DrawioRack:
    def __init__(self):
        self._create_base_element()
        self.first_rack_x = 120
        self.first_rack_y = 60
        self.rack_margin_top = 21
        self.rack_margin_bottom = 22
        self.rack_space = 120
        self.rack_unit_height = 15
        self.rack_width = 204
        self.rack_table = {}

    def save_to_file(self, filename="rack_diagram.drawio"):
        tree = ET.ElementTree(self.root)
        tree.write(filename, encoding="utf-8", xml_declaration=True)
        print(f"Draw.io 文件已生成：{filename}")

    def _generate_random_id(self, length=8):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    def _create_base_element(self):
        self.root = ET.Element("mxfile")
        self.root.set("host", "lszhang.com")
        now = datetime.now(timezone.utc)
        iso_format = now.replace(microsecond=0).isoformat()
        iso_format_z = iso_format.replace("+00:00", "Z")
        self.root.set("modified", iso_format_z)
        self.root.set("agent", "Python Script")
        self.root.set("version", "26.0.9")

        diagram = ET.SubElement(self.root, "diagram")
        diagram.set("name", "Rack Diagram")
        diagram.set("id", "rack-diagram")

        mx_graph_model = ET.SubElement(diagram, "mxGraphModel")
        mx_graph_model.set("dx", "1100")
        mx_graph_model.set("dy", "810")
        mx_graph_model.set("grid", "1")
        mx_graph_model.set("gridSize", "5")
        mx_graph_model.set("guides", "1")
        mx_graph_model.set("tooltips", "1")
        mx_graph_model.set("connect", "1")
        mx_graph_model.set("arrows", "1")
        mx_graph_model.set("fold", "1")
        mx_graph_model.set("page", "1")
        mx_graph_model.set("pageScale", "1")
        mx_graph_model.set("pageWidth", "1169")
        mx_graph_model.set("pageHeight", "827")
        mx_graph_model.set("math", "0")
        mx_graph_model.set("shadow", "0")

        self.root_element = ET.SubElement(mx_graph_model, "root")

        id0 = ET.SubElement(self.root_element, "mxCell")
        id0.set("id", "0")

        id1 = ET.SubElement(self.root_element, "mxCell")
        id1.set("id", "1")
        id1.set("parent", "0")

    def create_rack(self, rack_name="Rack", unit_count=42):
        rack_count_in_draw = len(self.rack_table)
        rack_x = self.first_rack_x + rack_count_in_draw * (self.rack_width + self.rack_space)
        rack_y = self.first_rack_y

        random_id = "rack_" + self._generate_random_id()
        self.rack_table[rack_name] = [random_id, unit_count]

        rack = ET.SubElement(self.root_element, "mxCell")
        rack.set("id", random_id)
        rack.set("value", rack_name)

        style = (
            f"strokeColor=#666666;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;"
            f"verticalAlign=top;outlineConnect=0;shadow=0;dashed=0;shape=mxgraph.rackGeneral.rackCabinet3;"
            f"fillColor2=#f4f4f4;container=1;collapsible=0;childLayout=rack;allowGaps=1;marginLeft=33;"
            f"marginRight=9;marginTop={self.rack_margin_top};marginBottom={self.rack_margin_bottom};"
            f"textColor=#666666;numDisp=descend;rackUnitSize={self.rack_unit_height};"
        )
        rack.set("style", style)
        rack.set("vertex", "1")
        rack.set("parent", "1")

        rack_geometry = ET.SubElement(rack, "mxGeometry")
        rack_geometry.set("x", str(rack_x))
        rack_geometry.set("y", str(rack_y))
        rack_geometry.set("width", str(self.rack_width))
        rack_height = self.rack_unit_height * unit_count + self.rack_margin_top + self.rack_margin_bottom
        rack_geometry.set("height", str(rack_height))
        rack_geometry.set("as", "geometry")

    def create_server(self, server_name, rack_name, floor_in_rack, height, ip='', purpose='', status='', other_data=''):
        if rack_name not in self.rack_table:
            self.create_rack(rack_name)
        rack_id = self.rack_table[rack_name][0]

        server_id = "server_" + self._generate_random_id()

        server_object = ET.SubElement(self.root_element, "object")
        server_object.set("id", server_id)
        server_object.set("label", server_name)

        if ip:
            server_object.set("IP", ip)
        if purpose:
            server_object.set("用途", purpose)
        if status:
            server_object.set("状态", status)

        if other_data:
            pairs = other_data.split('|')
            for pair in pairs:
                key, value = pair.split(':')
                key = key.strip()
                value = value.strip()
                server_object.set(key, value)

        server = ET.SubElement(server_object, "mxCell")
        shape_unit = 1
        if height >= 2:
            shape_unit = 2
        style = (
            f"strokeColor=#666666;html=1;labelPosition=right;align=left;spacingLeft=15;shadow=0;dashed=0;"
            f"outlineConnect=0;shape=mxgraph.rack.general.{shape_unit}u_rack_server;"
        )
        server.set("style", style)
        server.set("vertex", "1")
        server.set("parent", rack_id)

        server_geometry = ET.SubElement(server, "mxGeometry")
        server_geometry.set("x", "33")
        this_rack_unit_count = self.rack_table[rack_name][1]
        y = self.rack_margin_top + (this_rack_unit_count - floor_in_rack - height + 1) * self.rack_unit_height
        server_geometry.set("y", str(y))
        server_geometry.set("width", "162")
        server_geometry.set("height", str(height * self.rack_unit_height))
        server_geometry.set("as", "geometry")