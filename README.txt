Here is my working solution for the "color queueing" coding exercise.

Dependencies:  pip install tornado

I'm using Python Tornado because it has a good built-in web server that makes it easy to demonstrate prototypes without external dependencies.

1)  Set up a queue in the backend:
        a)  Using a dequeue (double ended queue) Python object to make re-queuing unused tuples more efficient.
        b)  Generates a list of integers from 0-255, then randomly selects three times from that list for each RGB color tuple being produced.
        c)  Every GET request checks the queue to determine if it is below 20% full and replenishes if necessary.
        
2)  Serve a simple web page with two buttons:
        a)  Using JQuery to handle AJAX requests and control button behaviors.
        b)  Data fetched from the queue is stashed within the html body using JQuery.data(). 
        c)  All requests are handled via GET methods to the Tornado back end.
        d)  The Fetch button activates a setTimeout function that is subsequently cleared if Set it clicked before 15 seconds.
        e)  Unused tuples are re-queued to the left end of the queue for later use.
        
3)  Once a tuple is delivered to a client, the backend must not serve that instance to another client for 15 seconds.
        a)  This was a bit tricky at first because #2 instructs you to "discard the (unused) tuple", whereas #3 says it should "return to the queue".  I interpreted this to mean that the front end should simply discard and unused tuple and only send a status update to the back end, whereas the backend should retain the tuple until intructed whether to requeue or discard.
        b)  I tried this another way by having the "timeout" method post the unused tuple back to the API for requeing.  This simplified coordinating requests across multiple clients, however, I decided this approach had two distinct disadvantages:
                1)  Clients who terminate before the timeout will never re-post their unused tuple, so those tuples would be lost forever.
                2)  Posting data back from the client introduces risks for string injection and corrupt values.  Since we specifically need three integers to define an RGB tuple, converting string values from the POST data back into integers seemed risky.

Thanks!
Steve Heinz