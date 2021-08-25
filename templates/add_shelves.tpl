% # Add shelves
<form action="/add/shelves/" method="POST" enctype="multipart/form-data">
	<table>
		<tr bgcolor="#AAAAAA"><th>Room</th><th>Shelves ID</th><th>Shelves Name</th></tr>
		<tr>
			<th><select name="selected_room_id" value="0">
					% for r in listRooms:
						<option value={{r[0]}}>{{r[1]}}</option>
					% end
				</select>
			</th>
	
	
			<th><input type="text" size="25"  name="new_shelves_id"></th>
			<th><input type="text" size="50"  name="new_shelves_name"></th>
		</tr>
		<tr>
			<th><input type="submit" name="button_add_shelves" value="Add new shelves"></th>
		</tr>
	</table>
</form>