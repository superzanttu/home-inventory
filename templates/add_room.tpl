% # Add room
<form action="/add/room/" method="POST" enctype="multipart/form-data">
	<table>
		<tr bgcolor="#AAAAAA"><th>Building</th><th>Room ID</th><th>Room Name</th></tr>
		<tr>
			<th><select name="selected_building_id" value="0">
					% for b in listBuildings:
						<option value={{b[0]}}>{{b[1]}}</option>
					% end
				</select>
			</th>
	
	
			<th><input type="text" size="25"  name="new_room_id"></th>
			<th><input type="text" size="50"  name="new_room_name"></th>
		</tr>
		<tr>
			<th><input type="submit" name="button_add_room" value="Add new room"></th>
		</tr>
	</table>
</form>