% # Edit single annotation
% annoTypes=[["TEXT","Text"],["LIST","List (select list id)"],["DATE","Date (yyy-mm-dd)"]]
% annoStatuses=[["0","Hidden"],["1","Visible"]]
<form action="/annotations/edit/{{editAnnotationID}}" method="POST" enctype="multipart/form-data">
	<table>
		<tr bgcolor="#AAAAAA">
			<th>ID</th>
			<th>Type</th>
			<th>List ID</th>
			<th>Text</th>
			<th>Status</th>
			<th>Actions</th>
		</tr>
		<tr>
			<th>{{editAnnotationID}}</th>
			<th>{{editAnnotationType}}</th>
			<th>{{editAnnotationListID}}</th>
			<th>{{editAnnotationText}}</th>
			<th>{{editAnnotationStatus}}</th>
		</tr>	
		<tr>
			<th><input type="text" name="new_annotation_id" value="{{editAnnotationID}}" readonly></th>
			<th><select name="new_annotation_type" value="0">
					% for a in annoTypes:
						% if a[0] == editAnnotationType:
							<option selected value={{a[0]}}>{{a[1]}}</option>
						% else:
							<option value={{a[0]}}>{{a[1]}}</option>
						% end
					% end
				</select>
			</th>
			<th><select name="new_annotation_list_id" value="0">
					<option value="">Not a list</option>
					% for a in listAnnoListIDs:
						% if a[0] == editAnnotationListID:
							<option selected value={{a[0]}}>{{a[0]}}</option>
						% else:
							<option value={{a[0]}}>{{a[0]}}</option>
						% end
					% end
				</select>
			</th>
			<th><input type="text" name="new_annotation_text" value="{{editAnnotationText}}"></th>
			<th><select name="new_annotation_status" value="0">
					% for a in annoStatuses:
						% if a[0] == editAnnotationStatus:
							<option selected value={{a[0]}}>{{a[1]}}</option>
						% else:
							<option value={{a[0]}}>{{a[1]}}</option>
						% end
					% end
				</select>
			</th>
			<th>
				<input type="submit" name="button_annotation_edit_save" value="Save">
				<input type="reset" name="button_annotation_edit_cancel" value="Reset">
			</th>
		</tr>	
	</table>
</from>
