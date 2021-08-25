% # List annotation lists
% annoStatuses={ "0":"Hidden", "1":"Visible" }
% import urllib.parse
<table>
	<tr bgcolor="#AAAAAA">
		<th>List ID</th>
		<th>Item</th>
		<th>Actions</th>
	</tr>
	% for a in listAnnotationListItems:
		<tr>
			<th>{{a[0]}}</th>
			<th>{{a[1]}}</th>
			<th>
				<table>
					<tr>
						<th>
							% q = urllib.parse.urlencode({ 'delete_listID' : a[0], 'delete_itemID' : a[1] })
							<form action="/annotation_list_item/delete/?{{q}}" method="POST" enctype="multipart/form-data">
								<button type="submit" name="button_annotationlist_item_delete_start" value="DELETE">Delete</button>
							</form>
						</th>
						<th>
							% q = urllib.parse.urlencode({ 'edit_listID' : a[0], 'edit_itemID' : a[1] })
							<form action="/annotation_list_item/edit/?{{q}}" method="POST" enctype="multipart/form-data">
								<button type="submit" name="button_annotationlist_item_edit_start" value="EDIT">Edit</button>
							</form>
						</th>
					</tr>
				</table>
			</th>
		</tr>
	% end
</table>

% # Add new annotation lists item
<form action="/annotation_list_item/add/" method="POST" enctype="multipart/form-data">
	<table>
		<tr bgcolor="#AAAAAA">
			<th>ID</th>
			<th>Item</th>
			<th>Actions</th>
		</tr>
		<tr>
			<th><select name="new_annotation_list_id">
					<option value="">Not selected</option>
					% for l in listAnnotationLists:
						<option value="{{l[0]}}">{{l[0]}}</option>
					% end
				</select>
			</th>

			<th><input type="text" name="new_annotationlist_item_text"></th>
			<th><input type="submit" name="button_annotationlist_item_add" value="Add new annotation list item"></th>
		</tr>	
	</table>
</from>

