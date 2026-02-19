import math
from arcade.geometry import are_polygons_intersecting


class WorldPhysicsEngine:
    """Simple impulse-based world physics for polygon hit boxes."""

    def __init__(self, game, collision_lists, world_bounds=None, iterations=4):
        self.game = game
        self.collision_lists = collision_lists
        self.world_bounds = world_bounds
        self.iterations = max(1, int(iterations))
        self.penetration_slop = 0.01
        self.position_correction = 0.8

    def update(self):
        bodies = self._collect_bodies()
        if not bodies:
            return

        for _ in range(self.iterations):
            self._resolve_world_bounds(bodies)
            self._resolve_collisions(bodies)

        self._sync_bodies(bodies)

    def _collect_bodies(self):
        bodies = []
        seen = set()
        for sprite_list in self.collision_lists:
            for body in sprite_list:
                if id(body) in seen:
                    continue
                seen.add(id(body))

                if not getattr(body, "collision_enabled", False):
                    continue
                if not all(hasattr(body, attr) for attr in ("x", "y", "move_x", "move_y")):
                    continue

                bodies.append(body)
        return bodies

    def _resolve_world_bounds(self, bodies):
        if not self.world_bounds:
            return

        left, right, bottom, top = self.world_bounds
        for body in bodies:
            if self._inverse_mass(body) == 0:
                continue

            min_off_x, max_off_x, min_off_y, max_off_y = self._hit_box_offsets(body)
            restitution = self._restitution(body)
            moved = False

            if body.x + min_off_x < left:
                body.x = left - min_off_x
                moved = True
                if body.move_x < 0:
                    body.move_x = -body.move_x * restitution
            elif body.x + max_off_x > right:
                body.x = right - max_off_x
                moved = True
                if body.move_x > 0:
                    body.move_x = -body.move_x * restitution

            if body.y + min_off_y < bottom:
                body.y = bottom - min_off_y
                moved = True
                if body.move_y < 0:
                    body.move_y = -body.move_y * restitution
            elif body.y + max_off_y > top:
                body.y = top - max_off_y
                moved = True
                if body.move_y > 0:
                    body.move_y = -body.move_y * restitution

            if moved:
                self._sync_body(body)

    def _resolve_collisions(self, bodies):
        for i in range(len(bodies) - 1):
            body_a = bodies[i]
            for j in range(i + 1, len(bodies)):
                body_b = bodies[j]
                self._resolve_pair(body_a, body_b)

    def _resolve_pair(self, body_a, body_b):
        points_a = self._hit_box_points(body_a)
        points_b = self._hit_box_points(body_b)
        if not points_a or not points_b:
            return

        if not are_polygons_intersecting(points_a, points_b):
            return

        normal_x, normal_y = self._collision_normal(body_a, body_b)

        penetration = self._axis_overlap(points_a, points_b, normal_x, normal_y)
        if penetration <= 0.0:
            penetration = 0.01
        inv_mass_a = self._inverse_mass(body_a)
        inv_mass_b = self._inverse_mass(body_b)
        inv_mass_sum = inv_mass_a + inv_mass_b
        if inv_mass_sum <= 0:
            return

        correction = (
            max(penetration - self.penetration_slop, 0.0)
            / inv_mass_sum
            * self.position_correction
        )
        body_a.x -= normal_x * correction * inv_mass_a
        body_a.y -= normal_y * correction * inv_mass_a
        body_b.x += normal_x * correction * inv_mass_b
        body_b.y += normal_y * correction * inv_mass_b
        self._sync_body(body_a)
        self._sync_body(body_b)

        relative_vx = body_b.move_x - body_a.move_x
        relative_vy = body_b.move_y - body_a.move_y
        velocity_normal = relative_vx * normal_x + relative_vy * normal_y
        if velocity_normal > 0:
            return

        restitution = min(self._restitution(body_a), self._restitution(body_b))
        impulse_magnitude = -((1.0 + restitution) * velocity_normal) / inv_mass_sum
        impulse_x = normal_x * impulse_magnitude
        impulse_y = normal_y * impulse_magnitude
        body_a.move_x -= impulse_x * inv_mass_a
        body_a.move_y -= impulse_y * inv_mass_a
        body_b.move_x += impulse_x * inv_mass_b
        body_b.move_y += impulse_y * inv_mass_b

        relative_vx = body_b.move_x - body_a.move_x
        relative_vy = body_b.move_y - body_a.move_y
        tangent_x = relative_vx - (relative_vx * normal_x + relative_vy * normal_y) * normal_x
        tangent_y = relative_vy - (relative_vx * normal_x + relative_vy * normal_y) * normal_y
        tangent_length = math.hypot(tangent_x, tangent_y)
        if tangent_length <= 1e-12:
            return

        tangent_x /= tangent_length
        tangent_y /= tangent_length
        friction_magnitude = -((relative_vx * tangent_x) + (relative_vy * tangent_y)) / inv_mass_sum
        max_friction = impulse_magnitude * math.sqrt(self._friction(body_a) * self._friction(body_b))
        friction_magnitude = max(-max_friction, min(friction_magnitude, max_friction))

        friction_x = tangent_x * friction_magnitude
        friction_y = tangent_y * friction_magnitude
        body_a.move_x -= friction_x * inv_mass_a
        body_a.move_y -= friction_y * inv_mass_a
        body_b.move_x += friction_x * inv_mass_b
        body_b.move_y += friction_y * inv_mass_b

    def _sync_bodies(self, bodies):
        for body in bodies:
            self._sync_body(body)

    @staticmethod
    def _sync_body(body):
        if hasattr(body, "sync_view_position"):
            body.sync_view_position()

    @staticmethod
    def _hit_box_points(body):
        if not hasattr(body, "hit_box") or body.hit_box is None:
            return None
        return body.hit_box.get_adjusted_points()

    def _hit_box_offsets(self, body):
        points = self._hit_box_points(body)
        if not points:
            radius = self._radius(body)
            return -radius, radius, -radius, radius

        center_x = body.center_x
        center_y = body.center_y
        min_off_x = min(point[0] - center_x for point in points)
        max_off_x = max(point[0] - center_x for point in points)
        min_off_y = min(point[1] - center_y for point in points)
        max_off_y = max(point[1] - center_y for point in points)
        return min_off_x, max_off_x, min_off_y, max_off_y

    @staticmethod
    def _collision_normal(body_a, body_b):
        dx = body_b.x - body_a.x
        dy = body_b.y - body_a.y
        distance = math.hypot(dx, dy)
        if distance > 1e-12:
            return dx / distance, dy / distance

        rel_x = body_b.move_x - body_a.move_x
        rel_y = body_b.move_y - body_a.move_y
        rel_len = math.hypot(rel_x, rel_y)
        if rel_len > 1e-12:
            return rel_x / rel_len, rel_y / rel_len

        return 1.0, 0.0

    @staticmethod
    def _axis_overlap(points_a, points_b, axis_x, axis_y):
        proj_a = [point[0] * axis_x + point[1] * axis_y for point in points_a]
        proj_b = [point[0] * axis_x + point[1] * axis_y for point in points_b]

        min_a = min(proj_a)
        max_a = max(proj_a)
        min_b = min(proj_b)
        max_b = max(proj_b)

        return min(max_a, max_b) - max(min_a, min_b)

    @staticmethod
    def _radius(body):
        radius = getattr(body, "collision_radius", None)
        if radius is not None:
            return max(float(radius), 1.0)
        default_radius = max(getattr(body, "width", 0), getattr(body, "height", 0)) / 2
        return max(default_radius, 8.0)

    @staticmethod
    def _inverse_mass(body):
        if getattr(body, "collision_static", False):
            return 0.0
        mass = max(float(getattr(body, "mass", 1.0)), 1e-6)
        return 1.0 / mass

    @staticmethod
    def _restitution(body):
        return max(0.0, min(1.0, float(getattr(body, "collision_restitution", 0.5))))

    @staticmethod
    def _friction(body):
        return max(0.0, float(getattr(body, "collision_friction", 0.2)))
