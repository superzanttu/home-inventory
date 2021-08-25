% # Add item
<form action="/add/item/" method="POST" enctype="multipart/form-data">
	<table>
		<tr bgcolor="#AAAAAA"><th>Container</th><th>Item ID</th><th>Item Name</th></tr>
		<tr>
			<th><select name="selected_container_id" value="0">
					% for s in listContainers:
						<option value={{s[0]}}>{{s[1]}}</option>
					% end
				</select>
			</th>
	
			<th><input type="text" size="25"  name="new_item_id"></th>
			<th><input type="text" size="50"  name="new_item_name"></th>
		</tr>
		<tr>
			<th><input type="submit" name="button_add_item" value="Add new item"></th>
		</tr>
	</table>
</form>