% # Delete item
<form action="/delete/item/" method="POST" enctype="multipart/form-data">
	<table>
		<tr bgcolor="#AAAAAA"><th>Item</th><th>Confirmation</th></tr>
		<tr>
			<th><select name="selected_item_id" value="0">
					% for i in listItems:
						<option value={{i[0]}}>{{i[1]}}</option>
					% end
				</select>
			</th>
	
			<th><input type="text" size="25"  name="confirmation_to_delete"></th>
		</tr>
		<tr>
			<th><input type="submit" name="button_delete_item" value="Delete item"></th>
		</tr>
	</table>
	<p>Enter item id to approve deletion.</p>
</form>