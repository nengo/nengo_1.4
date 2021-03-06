.. java:import:: java.io Serializable

.. java:import:: ca.nengo.model Node

.. java:import:: ca.nengo.model Resettable

.. java:import:: ca.nengo.model StructuralException

.. java:import:: ca.nengo.model Termination

.. java:import:: ca.nengo.util TimeSeries1D

SynapticIntegrator
==================

.. java:package:: ca.nengo.model.neuron
   :noindex:

.. java:type:: public interface SynapticIntegrator extends Resettable, Serializable, Cloneable

   Model of synaptic integration in a dendritic tree and soma.

   The model receives input from external sources (normally other neurons) and produces a net current which can be fed into a \ ``SpikeGenerator``\  and/or can produce other outputs of a Neuron.

   :author: Bryan Tripp

Methods
-------
clone
^^^^^

.. java:method:: public SynapticIntegrator clone() throws CloneNotSupportedException
   :outertype: SynapticIntegrator

   :throws CloneNotSupportedException: if clone can't be made
   :return: Valid clone

getTermination
^^^^^^^^^^^^^^

.. java:method:: public Termination getTermination(String name) throws StructuralException
   :outertype: SynapticIntegrator

   :param name: Name of a Termination onto this SynapticIntegrator
   :throws StructuralException: if the named Termination does not exist
   :return: The named Termination if it exists

getTerminations
^^^^^^^^^^^^^^^

.. java:method:: public Termination[] getTerminations()
   :outertype: SynapticIntegrator

   :return: List of distinct inputs (eg sets of synapses from different ensembles).

run
^^^

.. java:method:: public TimeSeries1D run(float startTime, float endTime)
   :outertype: SynapticIntegrator

   Runs the model for a given time interval. Input to each Termination should be set prior to calling this method, and is held constant during a run.

   The model is responsible for maintaining its internal state, and the state is assumed to be consistent with the start time. That is, if a caller calls run(0, 1, ...) and then run(5, 6, ...), the results may not make any sense, but this is not the model's responsibility. Start and end times are provided to support explicitly time-varying models, and for the convenience of Probeable models.

   Note that a run(...) is expected to cover a very short interval of time, e.g. 1/2 ms, during which inputs can be assumed to be constant. Normally a number of neurons in a network will run for this short length of time, possibly with diverse or varying internal time steps, and at the end of this time will communicate spikes to each other and then start again.

   :param startTime: Simulation time at which running starts (s)
   :param endTime: Simulation time at which running ends (s)
   :return: Time series of net current, including at least the start and end times, and optionally other times. Generally speaking additional values should be provided if the current varies substantially during the interval, but it is left to the implementation to interpret 'substantially'.

setNode
^^^^^^^

.. java:method:: public void setNode(Node node)
   :outertype: SynapticIntegrator

   This method should be called by the neuron that incorporates this SynapticIntegrator (Terminations need a reference to this).

   :param node: The node to which the SynapticIntegrator belongs

