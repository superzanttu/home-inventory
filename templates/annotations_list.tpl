% # List annotations
% annoTypes={ "TEXT":"Text", "LIST": "List", "DATE":"Date" }
% annoStatuses={ "0":"Hidden", "1":"Visible" }
<table>
	<tr bgcolor="#AAAAAA">
		<th>ID</th>
		<th>Type</th>
		<th>List ID</th>
		<th>Text</th>
		<th>Status</th>
		<th>Actions</th>
	</tr>
	% for a in listAnnotations:
		<tr>
			<th>{{a[0]}}</th>
			<th>{{annoTypes[a[1]]}}</th>
			<th>{{a[2]}}</th>
			<th>{{a[3]}}</th>
			<th>{{annoStatuses[a[4]]}}</th>
			<th>
				<table>
					<tr>
						<th>
							<form action="/annotations/delete/{{a[0]}}" method="POST" enctype="multipart/form-data">
								<button type="submit" name="button_annotation_delete_start" value="{{a[0]}}">Delete</button>
							</form>
						</th>
						<th>
							<form action="/annotations/edit/{{a[0]}}" method="POST" enctype="multipart/form-data">
								<button type="submit" name="button_annotation_edit_start" value="{{a[0]}}">Edit</button>
							</form>
						</th>
					</tr>
				</table>
			</th>
		</tr>
	% end
</table>


% # Add new annotation
<form action="/annotations/add/" method="POST" enctype="multipart/form-data">
	<table>
		<tr bgcolor="#AAAAAA">
			<th>ID</th>
			<th>Type</th>
			<th>List ID</th>
			<th>Create new list ID</th>
			<th>Text</th>
			<th>Status</th>
			<th>Actions</th>
		</tr>
		<tr>
			<th>Auto selected</th>
			<th><select name="new_annotation_type">
					<option value="TEXT">Text</option>
					<option value="LIST">List</option>
					<option value="DATE">Date</option>
				</select>
			</th>

			<th><select name="new_annotation_list_id">
					<option value="">Not needed</option>
					<option value="_CREATE_NEW_">Create new</option>
					% for l in listAnnotationLists:
						<option value="{{l[0]}}">{{l[0]}}</option>
					% end
				</select>
			</th>
			<th><input type="text" name="new_annotation_list_id_create"></th>

			<th><input type="text" name="new_annotation_text"></th>
			<th><select name="new_annotation_status">
					<option value="0">Hidden</option>
					<option value="1" selected>Visible</option>
				</select>
			</th>
			<th><input type="submit" name="button_add_new_annotation" value=Add new annotation"></th>
		</tr>	
	</table>
</from>
