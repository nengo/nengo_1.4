/*
The contents of this file are subject to the Mozilla Public License Version 1.1 
(the "License"); you may not use this file except in compliance with the License. 
You may obtain a copy of the License at http://www.mozilla.org/MPL/

Software distributed under the License is distributed on an "AS IS" basis, WITHOUT
WARRANTY OF ANY KIND, either express or implied. See the License for the specific 
language governing rights and limitations under the License.

The Original Code is "Rectifier.java". Description: 
"Wraps an underlying VectorGenerator, rectifying generated vectors before 
  they are returned"

The Initial Developer of the Original Code is Bryan Tripp & Centre for Theoretical Neuroscience, University of Waterloo. Copyright (C) 2006-2008. All Rights Reserved.

Alternatively, the contents of this file may be used under the terms of the GNU 
Public License license (the GPL License), in which case the provisions of GPL 
License are applicable  instead of those above. If you wish to allow use of your 
version of this file only under the terms of the GPL License and not to allow 
others to use your version of this file under the MPL, indicate your decision 
by deleting the provisions above and replace  them with the notice and other 
provisions required by the GPL License.  If you do not delete the provisions above,
a recipient may use your version of this file under either the MPL or the GPL License.
*/

/*
 * Created on 27-Jul-2006
 */
package ca.nengo.util.impl;

import ca.nengo.util.VectorGenerator;

/**
 * Wraps an underlying VectorGenerator, rectifying generated vectors before 
 * they are returned. 
 * 
 * @author Bryan Tripp
 */
public class Rectifier implements VectorGenerator {

	private VectorGenerator myVG;
	private boolean myPositiveFlag = true;
	
	/**
	 * @param vg A VectorGenerator to underlie this one (ie to produce non-rectified vectors)
	 */
	public Rectifier(VectorGenerator vg) {
		this(vg, true);
	}
	
	/**
	 * @param vg A VectorGenerator to underlie this one (ie to produce non-rectified vectors)
	 * @param positive True: vectors are rectified; false: vectors are anti-rectified
	 */
	public Rectifier(VectorGenerator vg, boolean positive) {
		myVG = vg;
		myPositiveFlag = positive; 
	}
	
	/**
	 * @return Underlying vector generator (output of which is rectified)
	 */
	public VectorGenerator getRectified() {
		return myVG;
	}
	
	/**
	 * 
	 * @param vg New underlying vector generator (output of which is to be rectified)
	 */
	public void setRectified(VectorGenerator vg) {
		myVG = vg;
	}

	/**
	 * @return True if values are rectified to be >= 0; false if rectified to <= 0 
	 */
	public boolean getPositive() {
		return myPositiveFlag;
	}
	
	/**
	 * @param positive True if values are rectified to be >= 0; false if rectified to <= 0
	 */
	public void setPositive(boolean positive) {
		myPositiveFlag = positive;
	}

	/**
	 * @return Rectified version of vector generated by underlying VectorGenerator
	 * 		(all components -> abs value) 
	 *  
	 * @see ca.nengo.util.VectorGenerator#genVectors(int, int)
	 */
	public float[][] genVectors(int number, int dimension) {
		float[][] raw = myVG.genVectors(number, dimension);
		float[][] result = new float[raw.length][];
		
		for (int i = 0; i < raw.length; i++) {
			result[i] = new float[raw[i].length];
			for (int j = 0; j < raw[i].length; j++) {
				result[i][j] = myPositiveFlag ? Math.abs(raw[i][j]) : - Math.abs(raw[i][j]);
			}
		}
		
		return result;
	}

}
