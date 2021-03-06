.. java:import:: java.io Serializable

Noise
=====

.. java:package:: ca.nengo.model
   :noindex:

.. java:type:: public interface Noise extends Cloneable, Resettable, Serializable

   An model of noise that can be explicitly injected into a circuit (e.g. added to an Origin).

   Noise may be cloned across independent dimensions of a Noisy. This means that either 1) noise parameters can't be changed after construction, or 2) parameters must be shared or propagated across clones.

   :author: Bryan Tripp

Fields
------
DIMENSION_PROPERTY
^^^^^^^^^^^^^^^^^^

.. java:field:: public static final String DIMENSION_PROPERTY
   :outertype: Noise

   How do we refer to the dimension?

Methods
-------
clone
^^^^^

.. java:method:: public Noise clone()
   :outertype: Noise

   :return: Valid clone

getValue
^^^^^^^^

.. java:method:: public float getValue(float startTime, float endTime, float input)
   :outertype: Noise

   :param startTime: Simulation time at which step starts
   :param endTime: Simulation time at which step ends
   :param input: Value which is to be corrupted by noise
   :return: The noisy values (inputs corrupted by noise)

