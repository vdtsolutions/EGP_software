
import math
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QPainter, QPen, QColor, QPainterPath

VISUAL_REF_RADIUS = 150
DEPTH_MOVED = {}  # injected from main


class CircleWidget(QWidget):
    def __init__(
        self,
        all_halls,
        working_halls,
        reference_values,
        depth_moved,
        visual_labels=None
    ):
        super().__init__()

        global DEPTH_MOVED
        DEPTH_MOVED = depth_moved

        self.visual_labels = visual_labels or {}

        # View controls
        self.zoom = 1.0
        self.zoom_step = 1.15
        self.min_zoom = 0.3
        self.max_zoom = 5.0
        self.pan_x = 0
        self.pan_y = 0
        self.last_mouse_pos = None

        self.all_halls = all_halls
        self.working_halls = list(working_halls)
        self.reference_values = reference_values

        self.points = {}

        # 🔒 ANGLES ONLY FOR WORKING HALLS (DO NOT TOUCH)
        angle_step = 360 / len(self.working_halls)
        for i, hall in enumerate(self.working_halls):
            self.points[hall] = {
                "angle": math.radians(i * angle_step - 90),
                "current_r": VISUAL_REF_RADIUS,
                "target_r": VISUAL_REF_RADIUS
            }

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(16)

        self.setMinimumHeight(400)

    # ------------------------
    # VISUAL LABEL
    # ------------------------
    def get_visual_label(self, hall):
        return self.visual_labels.get(hall, hall)

    # ------------------------
    # RESET
    # ------------------------
    def reset_points(self):
        for hall in self.working_halls:
            self.points[hall]["current_r"] = VISUAL_REF_RADIUS
            self.points[hall]["target_r"] = VISUAL_REF_RADIUS
        self.update()

    # ------------------------
    # LOGIC
    # ------------------------
    def set_target_values(self, measured_values):
        VISUAL_SCALE = 4
        for hall in self.working_halls:
            depth = DEPTH_MOVED.get(hall, 0) * VISUAL_SCALE
            self.points[hall]["target_r"] = VISUAL_REF_RADIUS - depth

    def animate(self):
        dirty = False
        for p in self.points.values():
            diff = p["target_r"] - p["current_r"]
            if abs(diff) > 0.3:
                p["current_r"] += diff * 0.2
                dirty = True
        if dirty:
            self.update()

    # ------------------------
    # DRAW
    # ------------------------
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        cx = self.width() // 2
        cy = self.height() // 2

        painter.translate(cx + self.pan_x, cy + self.pan_y)
        painter.scale(self.zoom, self.zoom)
        painter.translate(-cx, -cy)

        # ----------------------------------
        # BUILD EXACT CARTESIAN POINTS
        # ----------------------------------
        ordered = []
        for hall in self.working_halls:
            p = self.points[hall]
            a = p["angle"]
            r = p["current_r"]
            x = cx + r * math.cos(a)
            y = cy + r * math.sin(a)
            ordered.append((a, QPointF(x, y), hall, r))

        ordered.sort(key=lambda t: t[0])

        # ----------------------------------
        # RADIAL DENT CURVE (KEY FIX)
        # ----------------------------------
        path = QPainterPath()
        pts = ordered + [ordered[0]]  # close loop

        def radial_control(pt, r, scale=0.35):
            # inward normal (towards center)
            nx = cx - pt.x()
            ny = cy - pt.y()
            length = math.hypot(nx, ny) or 1.0
            nx /= length
            ny /= length

            # pull only if deformed
            d = (VISUAL_REF_RADIUS - r) * scale

            return QPointF(
                pt.x() + nx * d,
                pt.y() + ny * d
            )

        path.moveTo(pts[0][1])

        for i in range(1, len(pts)):
            _, p0, _, r0 = pts[i - 1]
            _, p1, _, r1 = pts[i]

            c0 = radial_control(p0, r0)
            c1 = radial_control(p1, r1)

            path.cubicTo(c0, c1, p1)

        painter.setPen(QPen(Qt.blue, 2))
        painter.drawPath(path)

        # ----------------------------------
        # DRAW POINTS + LABELS + DEPTH
        # ----------------------------------
        for a, pt, hall, r in ordered:
            x, y = pt.x(), pt.y()

            # green points
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor("#2ecc71"))
            painter.drawEllipse(int(x - 3), int(y - 3), 6, 6)

            # hall labels
            label = self.get_visual_label(hall)
            label_r = VISUAL_REF_RADIUS + 26

            lx = cx + label_r * math.cos(a)
            ly = cy + label_r * math.sin(a)

            angle_deg = math.degrees(a)
            if 90 < angle_deg < 270:
                angle_deg += 180

            painter.save()
            painter.translate(lx, ly)
            painter.rotate(angle_deg)
            painter.setPen(Qt.black)
            painter.drawText(-20, 6, label)
            painter.restore()

            # depth labels
            if abs(r - VISUAL_REF_RADIUS) > 1:
                depth = DEPTH_MOVED.get(hall, 0)
                dr = r - 18
                dx = cx + dr * math.cos(a)
                dy = cy + dr * math.sin(a)

                painter.save()
                painter.translate(dx, dy)
                painter.rotate(angle_deg)
                painter.setPen(QColor("#c0392b"))
                painter.drawText(-20, 6, f"{depth:.2f}")
                painter.restore()

    # ------------------------
    # INTERACTION
    # ------------------------
    def wheelEvent(self, event):
        self.zoom *= self.zoom_step if event.angleDelta().y() > 0 else 1 / self.zoom_step
        self.zoom = max(self.min_zoom, min(self.zoom, self.max_zoom))
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_mouse_pos = event.pos()

    def mouseMoveEvent(self, event):
        if self.last_mouse_pos:
            delta = event.pos() - self.last_mouse_pos
            self.pan_x += delta.x()
            self.pan_y += delta.y()
            self.last_mouse_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        self.last_mouse_pos = None
