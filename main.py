import pygame
import math
import random
import sys

pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulateur de Trou Noir & Lentille Gravitationnelle")
clock = pygame.time.Clock()

# Couleurs (Thème Espace Profond & Néon)
DARK_BG = (8, 10, 15)
WHITE = (255, 255, 255)
GRAY = (100, 110, 130)
BH_COLOR = (15, 18, 25)
ACCRETION_DISK = (255, 140, 0) # Disque d'accrétion orangé
LIGHT_COLOR = (0, 230, 255)    # Faisceaux lumineux cyan

# Polices
font_medium = pygame.font.SysFont("Arial", 20, bold=True)
font_small = pygame.font.SysFont("Arial", 15)

class BlackHole:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.mass = 4500     # Intensité de la gravité
        self.radius = 32     # Rayon de l'horizon des événements

black_hole = BlackHole(WIDTH // 2, HEIGHT // 2)

class LightRay:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.alive = True
        self.trail = []

rays = []

def spawn_rays_grid():
    global rays
    rays = []
    # Créer un flux de lumière horizontal venant de la gauche
    for y in range(80, HEIGHT - 80, 25):
        rays.append(LightRay(40, y, 6.0, 0.0))

spawn_rays_grid()

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Déplacer le trou noir là où l'on clique
            black_hole.x, black_hole.y = mouse_pos
            spawn_rays_grid()
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                spawn_rays_grid()

    # --- PHYSIQUE DE LA LENTILLE GRAVITATIONNELLE ---
    for ray in rays:
        if not ray.alive:
            continue

        # Calculer l'attraction gravitationnelle du trou noir sur le rayon lumineux
        dx = black_hole.x - ray.x
        dy = black_hole.y - ray.y
        dist_sq = dx**2 + dy**2 + 400  # Adoucissement
        dist = math.sqrt(dist_sq)

        # Si le rayon touche l'horizon des événements, il est capturé
        if dist < black_hole.radius:
            ray.alive = False
            continue

        # Déviation de la lumière (Effet Einstein)
        force = (black_hole.mass * 1.5) / dist_sq
        ray.vx += force * (dx / dist)
        ray.vy += force * (dy / dist)

        # Normaliser la vitesse pour qu'elle reste constante (vitesse de la lumière simulée)
        speed = math.hypot(ray.vx, ray.vy)
        if speed > 0:
            ray.vx = (ray.vx / speed) * 6.5
            ray.vy = (ray.vy / speed) * 6.5

        # Mettre à jour la position
        ray.x += ray.vx
        ray.y += ray.vy

        # Enregistrer la trajectoire pour créer un sillage lumineux
        ray.trail.append((int(ray.x), int(ray.y)))
        if len(ray.trail) > 25:
            ray.trail.pop(0)

        # Supprimer le rayon s'il sort de l'écran
        if not (0 <= ray.x <= WIDTH and 0 <= ray.y <= HEIGHT):
            ray.alive = False

    # Régénérer les rayons en continu pour un flux permanent
    if random.random() < 0.3 and len(rays) < 50:
        y_spawn = random.randint(80, HEIGHT - 80)
        rays.append(LightRay(40, y_spawn, 6.0, 0.0))

    screen.fill(DARK_BG)

    # 1. Dessiner les sillages lumineux et les rayons
    for ray in rays:
        if len(ray.trail) > 1:
            pygame.draw.aalines(screen, LIGHT_COLOR, False, ray.trail)

    # 2. Dessiner le Trou Noir et son disque d'accrétion lumineux
    # Disque lumineux externe
    pygame.draw.circle(screen, ACCRETION_DISK, (black_hole.x, black_hole.y), black_hole.radius + 8, 3)
    # Ombre / Trou noir central (Noir absolu)
    pygame.draw.circle(screen, BH_COLOR, (black_hole.x, black_hole.y), black_hole.radius)
    pygame.draw.circle(screen, WHITE, (black_hole.x, black_hole.y), black_hole.radius, 1)

    # 3. En-tête HUD et Instructions
    title_txt = font_medium.render("SIMULATEUR DE TROU NOIR & LENTILLE GRAVITATIONNELLE", True, WHITE)
    screen.blit(title_txt, (WIDTH // 2 - title_txt.get_width() // 2, 18))

    inst_txt = font_small.render("CLIC GAUCHE : Déplacer le trou noir | R : Réinitialiser les rayons lumineux", True, GRAY)
    screen.blit(inst_txt, (WIDTH // 2 - inst_txt.get_width() // 2, 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()