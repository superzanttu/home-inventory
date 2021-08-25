% # Add box
<form action="/add/box/" method="POST" enctype="multipart/form-data">
	<table>
		<tr bgcolor="#AAAAAA"><th>Room or Shelf</th><th>Box ID</th><th>Box Name</th></tr>
		<tr>
			<th><select name="selected_shelf_id" value="0">
					% for s in listShelfs:
						<option value={{s[0]}}>{{s[1]}}</option>
					% end
				</select>
			</th>
	
			<th><input type="text" size="25"  name="new_box_id"></th>
			<th><input type="text" size="50"  name="new_box_name"></th>
		</tr>
		<tr>
			<th><input type="submit" name="button_add_box" value="Add new box"></th>
		</tr>
	</table>
</form>