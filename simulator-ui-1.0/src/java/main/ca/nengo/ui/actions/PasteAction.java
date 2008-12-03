/*
The contents of this file are subject to the Mozilla Public License Version 1.1 
(the "License"); you may not use this file except in compliance with the License. 
You may obtain a copy of the License at http://www.mozilla.org/MPL/

Software distributed under the License is distributed on an "AS IS" basis, WITHOUT
WARRANTY OF ANY KIND, either express or implied. See the License for the specific 
language governing rights and limitations under the License.

The Original Code is "PasteAction.java". Description: 
""

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

package ca.nengo.ui.actions;

import ca.nengo.model.Node;
import ca.nengo.ui.NengoGraphics;
import ca.nengo.ui.models.NodeContainer;
import ca.nengo.ui.models.NodeContainer.ContainerException;
import ca.shu.ui.lib.actions.ActionException;
import ca.shu.ui.lib.actions.StandardAction;

public class PasteAction extends StandardAction {

	private static final long serialVersionUID = 1L;

	private NodeContainer nodeContainer;

	public PasteAction(String description, NodeContainer nodeContainer) {
		super(description);

		this.nodeContainer = nodeContainer;
	}

	@Override
	protected void action() throws ActionException {
		Node node = NengoGraphics.getInstance().getClipboard().getContents();
		if (node != null) {
			try {
				CreateModelAction.ensureNonConflictingName(node, nodeContainer);
				nodeContainer.addNodeModel(node);
			} catch (ContainerException e) {
				throw new ActionException(e);
			}
		} else {
			throw new ActionException("Clipboard is empty");
		}
	}
}