class Controller:
    """ This class handles controll between the view (what the user see's) and the model (the simulation)
    """

    def __init__(self, model, view):
        """__init__ creates a controller

        Args:
            model (Simulation object): The simulation that will be run
            view (view_ object): The way information from the simulation will be given to the user
        """
        self.view = view
        self.model = model

    def start(self):
        """start calls the setup function of the view and starts the view's mainloop
        """
        self.view.setup(self)
        self.view.start_mainloop()
