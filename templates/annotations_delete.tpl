% # Delete single annotation
% annoTypes={ "TEXT":"Text", "LIST": "List", "DATE":"Date" }
% annoStatuses={ "0":"Hidden", "1":"Visible" }

<form action="/annotations/delete/{{deleteAnnotationID}}" method="POST" enctype="multipart/form-data">
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
			<th>{{deleteAnnotationID}}</th>
			<th>{{deleteAnnotationType}}</th>
			<th>{{deleteAnnotationListID}}</th>
			<th>{{deleteAnnotationText}}</th>
			<th>{{deleteAnnotationStatus}}</th>
			<th>
				<input type="submit" name="button_annotation_delete_confirm" value="Delete">
				<input type="submit" name="button_annotation_delete_cancel" value="Cancel">
			</th>
		</tr>	
	</table>
</from>
