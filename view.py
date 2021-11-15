import pygame
from config import SIM_SETTINGS, WORLD_SETTINGS


class View:
    """ Master class for all view implementations
    """
    pass


class Pygame_view(View):
    """Pygame_view a view type utilizing the pygame module

    Args:
        View (View object): The master class for all view implementations
    """

    def setup(self, controller):
        """setup sets up the view object ready to be used:
        This means:
         - Init font that will be used
         - Init the clock for the simulation

        Args:
            controller ([type]): [description]
        """
        self.controller = controller
        pygame.init()
        self.my_font = pygame.font.SysFont('comicsansms', 15)

        self.screen = pygame.display.set_mode(
            [SIM_SETTINGS['WINDOW_WIDTH'], SIM_SETTINGS['WINDOW_HEIGHT']])
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.clock = pygame.time.Clock()

    def start_mainloop(self):
        """start_mainloop starts simulation and calls the main function
        """
        simulation_continue = True
        while(simulation_continue):
            # Run model mainloop
            self.controller.model.run_mainloop()

            # Draw background
            self.screen.fill((0, 41, 58))

            # Draw objects
            self.draw_objects()

            # Draw master controller stats
            self.draw_master_controller_stats()

            # Update screen
            pygame.display.flip()
            self.clock.tick(2)  # ToDo: Make this dynamic from config
            # Check for quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    simulation_continue = False
                    print("QUITTING SIMULATION")

    def draw_world_objects(self):
        """draw_world_objects loops through each world object in the simulation and draws it in the game world
        """
        for world_object in self.controller.model.objects:
            micro_x_position = (world_object.micro_x_position /
                                self.controller.model.MICRO_X_MAX) * SIM_SETTINGS['WINDOW_WIDTH']
            micro_y_position = (world_object.micro_y_position /
                                self.controller.model.MICRO_Y_MAX) * SIM_SETTINGS['WINDOW_HEIGHT']
            if(world_object.detected):
                colour = self.RED
            else:
                colour = self.GREEN
            pygame.draw.circle(self.screen, colour,
                               (micro_x_position, micro_y_position), (10))

    def draw_agents(self):
        """draw_agents loops through each agent in the simulation and draws it in the game world
        """
        for agent in self.controller.model.agents:
            micro_x_position = (agent.micro_x_position /
                                self.controller.model.MICRO_Y_MAX) * SIM_SETTINGS['WINDOW_WIDTH']
            micro_y_position = (agent.micro_y_position /
                                self.controller.model.MICRO_Y_MAX) * SIM_SETTINGS['WINDOW_HEIGHT']
            if(agent.agent_type == 'USV'):
                pygame.draw.rect(self.screen, self.RED,
                                 (micro_x_position, micro_y_position, 10, 7))
            elif(agent.agent_type == 'UAV'):
                pygame.draw.rect(self.screen, self.BLUE,
                                 (micro_x_position, micro_y_position, 10, 7))

    def draw_objects(self):
        """draw_objects draws all the objects in the world
        This means:
         - Drawing all of the world objects
         - Drawing all of the agents
        """
        self.draw_world_objects()
        self.draw_agents()

    def draw_master_controller_stats(self):
        """draw_master_controller_stats draws out the information from the master controller
        namely:
         - Found objects -- How many objects is the master controller aware of
         - Objects identified -- How many identified objects is the master controller aware of
         - Objects interacted -- How many objects is the master controller aware of that have been interacted with
         - Total objects --- How many objects is the master controller aware of in total
        """
        found = self.controller.model.master_controller.found_objects
        identified = self.controller.model.master_controller.objects_identified
        interacted = self.controller.model.master_controller.object_interacted
        total = self.controller.model.master_controller.total_objects
        master_controller_title = self.my_font.render(
            "Master controller stats:", True, (255, 255, 255))
        found_objects = self.my_font.render(
            f"{found} / {total} found objects", True, (255, 255, 255))
        identified_objects = self.my_font.render(
            f"{identified} / {total} identified objects", True, (255, 255, 255))
        interacted_objects = self.my_font.render(
            f"{interacted} / {total} interacted objects", True, (255, 255, 255))
        self.screen.blit(master_controller_title, (300, 20))
        self.screen.blit(found_objects, (320, 35))
        self.screen.blit(identified_objects, (320, 50))
        self.screen.blit(interacted_objects, (320, 65))
