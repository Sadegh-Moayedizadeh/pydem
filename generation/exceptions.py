"""Contains exception classes related to the generation process
"""

class SizeOutOfBound(Exception):
    """Should be raised when the given size of a particle while 
    constructing one is out of the specified boundaries in the
    correspong class

    Parents:
        Exception: the base class for exceptions
    """
    
    def __init__(self, message: str =''):
        """Initializing the error instance

        Args:
            message (str): the error message recieved while raising the
                exception
        """
        
        self.message = message