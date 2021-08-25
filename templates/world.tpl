% # World viewer
<table>
	<tr bgcolor="#AAAAAA">
		<th align="left">Buildings [0]</th>
		% if listRooms:
			<th align="left">Rooms [1]</th>
		% end
		% if listLevel1Objects:
			<th align="left">Shelves/Box/Room [2]</th>
		% end
		% if listLevel2Objects:		
			<th align="left">Shelf/Box/Room [3]</th>
		% end
		% if listLevel3Objects:		
			<th align="left">Shelf/Box/Room [4]</th>
		% end
		% if listLevel4Objects:
			<th align="left">Shelf/Box/Room [5]</th>
		% end
		% if listItems:
			<th align="left">Items in selected container</th>
		% end
		% if selectedItemInfo:
			<th align="left">Item info</th>
			<th align="left">Item annotations</th>
		% end
	</tr>
	<tr>
		
		% # Buildings
		% if listBuildings:
		%	worldPath="/world/"
			<th valign="top"><table>
		%	for b in listBuildings:
		%		if b['id']==lastSelectedObject:
					<tr bgcolor="#ccd1ff">
		%		elif b['id']==selectedBuilding:
					<tr bgcolor="#dddddd">
		%		else:
					<tr>
		%		end
						<th align="left">
							<a href="{{worldPath}}{{b['id']}}/">
								{{b['id'].title()}}
							</a>
							<a href="/modify/container_attributes/{{b['id']}}">
								[m]
							</a>
							</th>
					</tr>
		%	end
			</table></th>
		% end
		
		
		
		% # Rooms
		% if listRooms:
		%	worldPath="/world/"+selectedBuilding+"/"
			<th valign="top"><table>
		%	for b in listRooms:
		%		if b['id']==lastSelectedObject:
					<tr bgcolor="#ccd1ff">
		%		elif b['id']==selectedRoom:
					<tr bgcolor="#dddddd">
		%		else:
					<tr>
		%		end
						<th align="left">
							<a href="{{worldPath}}{{b['id']}}/">
								{{b['id'].title()}}
							</a>
							<a href="/modify/container_attributes/{{b['id']}}">
								[m]
							</a>
						</th>
					</tr>
		%	end
			</table></th>
		% end
		
		
		
		% # Level 1 objects
		% if listLevel1Objects:
		%	worldPath="/world/"+selectedBuilding+"/"+selectedRoom+"/"
			<th valign="top"><table>
		%	for b in listLevel1Objects:
		%		if b['id']==lastSelectedObject:
					<tr bgcolor="#ccd1ff">
		%		elif b['id']==selectedObjectLevel1:
					<tr bgcolor="#dddddd">
		%		else:
					<tr>
		%		end
						<th align="left">
							<a href="{{worldPath}}{{b['id']}}/">
								{{b['id'].title()}}
							</a>
							<a href="/modify/container_attributes/{{b['id']}}">
								[m]
							</a>
						</th>
						<th align="right">
							<font size=0>
								{{b['type']}}
							</font>
						</th>
					</tr>
		%	end
			</table></th>
		% end
		
	
		
		% # Level 2 objects
		% if listLevel2Objects:
		%	worldPath="/world/"+selectedBuilding+"/"+selectedRoom+"/"+selectedObjectLevel1+"/"
			<th valign="top"><table>
		%	for b in listLevel2Objects:
		%		if b['id']==lastSelectedObject:
					<tr bgcolor="#ccd1ff">
		%		elif b['id']==selectedObjectLevel2:
					<tr bgcolor="#dddddd">
		%		else:
					<tr>
		%		end
						<th align="left">
							<a href="{{worldPath}}{{b['id']}}/">
								{{b['id'].title()}}
							</a>
							<a href="/modify/container_attributes/{{b['id']}}">
								[m]
							</a>
						</th>
						<th align="right">
							<font size=0>
								{{b['type']}}
							</font>
						</th>
					</tr>
		%	end
			</table></th>
		% end
		
		
		
		% # Level 3 objects
		% if listLevel3Objects:
		%	worldPath="/world/"+selectedBuilding+"/"+selectedRoom+"/"+selectedObjectLevel1+"/"+selectedObjectLevel2+"/"
			<th valign="top"><table>
		%	for b in listLevel3Objects:
		%		if b['id']==lastSelectedObject:
					<tr bgcolor="#ccd1ff">
		%		elif b['id']==selectedObjectLevel3:
					<tr bgcolor="#dddddd">
		%		else:
					<tr>
		%		end
						<th>
							<a href="{{worldPath}}{{b['id']}}/">
								{{b['id'].title()}}
							</a>
							<a href="/modify/container_attributes/{{b['id']}}">
								[m]
							</a>
						</th>
						<th align="right">
							<font size=0>
								{{b['type']}}
							</font>
						</th>
					</tr>
						
		%	end
			</table></th>
		% end
		
		
		
		% # Level 4 objects
		% if listLevel4Objects:
		%	worldPath="/world/"+selectedBuilding+"/"+selectedRoom+"/"+selectedObjectLevel1+"/"+selectedObjectLevel2+"/"+selectedObjectLevel3+"/"
			<th valign="top"><table>
		%	for b in listLevel4Objects:
		%		if b['id']==lastSelectedObject:
					<tr bgcolor="#ccd1ff">
		%		elif b['id']==selectedObjectLevel4:
					<tr bgcolor="#dddddd">
		%		else:
					<tr>
		%		end
						<th>
							<a href="{{worldPath}}{{b['id']}}/">
								{{b['id'].title()}}
							</a>
							<a href="/modify/container_attributes/{{b['id']}}">
								[m]
							</a>
						</th>
						<th align="right">
							<font size=0>
								{{b['type']}}
							</font>
						</th>
					</tr>
		%	end
			</table></th>
		% end
	
		% # Recursively selected items
		% if listItems:
			<th valign="top"><table>
		%	for b in listItems:
		%		if b['container_id'] == lastSelectedObject:
					<tr bgcolor="ccd1ff">
						<th align="left">
							<a href="{{pageURL}}?selected_item_id={{b['id']}}">
								{{b['name'].title()}}
							</a>
						</th>
					</tr>
		%		end
		%	end
			</table>
			<table>
				<th align="left" bgcolor="#AAAAAA">Items in other containers</th>
		%	for b in listItems:
		%		if b['container_id'] != lastSelectedObject:
					<tr>
						<th align="left">
							<a href="{{pageURL}}?selected_item_id={{b['id']}}">
								{{b['name'].title()}}
							</a>
						</th>
					</tr>
		% 		end
		%	end
			</table></th>
		% end			
		
		% # Information about selected item
		% if selectedItemInfo:
			<th valign="top"><table>
		%	for i in selectedItemInfo:
				<tr>
					<th align="left">
						{{i[0]}}
					</th>
					<th align="right">
						{{i[1]}}
					</th>
				</tr>
		%	end		
				<tr><th align="left"><a href="/modify/item_attributes/{{querySelectedItemID}}">Modify</a></th></tr>
			</table></th>
			
		% 	# Annotations of item
			<th valign="top"><table>
		% 	if selectedItemAnnotations:
				
		%		for i in selectedItemAnnotations:
					<tr>
						<th align="left">
							{{i[0]}}
						</th>
						<th align="right">
							{{i[1]}}
						</th>
					</tr>
		%		end
		%	end
				<tr>
					<th><a href="/annotation/add/{{querySelectedItemID}}">Add</a></th>
					<th><a href="/annotation/modify/{{querySelectedItemID}}">Modify</a></th>
				</tr>
			</table></th>
		% end
		
		
	</tr>

</table>