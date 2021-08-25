% # Modify item attributes
<form action="/modify/item_attributes/{{modifyItemID}}" method="POST" enctype="multipart/form-data">
	<table>
		<tr bgcolor="#AAAAAA"><th>Item ID</th><th style="max-width:10%;">Container ID</th><th>Item Name</th></tr>
		<tr>
			<th><input type="text" name="new_item_id" value="{{modifyItemID}}"></th>
			<th><select name="new_container_id" value="0">
					% for c in listContainers:
						% if c[0]==modifyItemContainerID:
							<option selected value={{c[0]}}>{{c[1]}}</option>
						% else:
							<option value={{c[0]}}>{{c[1]}}</option>
						% end
					% end
				</select>
			</th>
			<th><input type="text" name="new_item_name" value="{{modifyItemName}}"></th>
		</tr>
		<tr>
			<th>
				<input type="submit" name="button_modify_item_attributes" value="Save changes">
				<input type="reset" name="button_reset_item_attributes" value="Reset values">
			</th>
		</tr>
	</table>
</form>