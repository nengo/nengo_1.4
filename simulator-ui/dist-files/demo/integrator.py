import nef

# Create the network object
net = nef.Network('Integrator')

# Create a controllable input function that
# goes to 5 at time 0.2s, to 0 at time 0.3s and so on
net.make_input('input', {0.2: 5, 0.3: 0, 0.44: -10, 0.54: 0, 0.8: 5, 0.9: 0})

# Make a population with 100 neurons, 1 dimension
net.make('A', 100, 1, quick=True)

# Connect the input to the integrator, scaling the input by .1;
# postsynaptic time constant is 100 ms
net.connect('input', 'A', weight=0.1, pstc=0.1)

# Connect the population to itself with the default weight of 1
net.connect('A', 'A', pstc=0.1)

net.add_to_nengo()
