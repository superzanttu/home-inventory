% # Add shelf
<form action="/add/shelf/" method="POST" enctype="multipart/form-data">
	<table>
		<tr bgcolor="#AAAAAA"><th>Shelves Name</th><th>Shelf column</th><th>Shelf row</th><th>Shelf name</th></tr>
		<tr>
			<th><select name="selected_shelves_id" value="0">
					% for s in listShelves:
						<option value={{s[0]}}>{{s[1]}}</option>
					% end
				</select>
			</th>
			<th><input type="text" size="25"  name="new_shelf_column"></th>
			<th><input type="text" size="25"  name="new_shelf_row"></th>
			<th><input type="text" size="50"  name="new_shelf_name"></th>
		</tr>
		<tr>
			<th><input type="submit" name="button_add_shelf" value="Add new shelf"></th>
		</tr>
	</table>
</form>