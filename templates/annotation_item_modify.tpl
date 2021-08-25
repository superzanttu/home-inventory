% # Modify item annotations
<form action="/annotation/modify/{{editItemID}}" method="POST" enctype="multipart/form-data">
	<table>
		<tr bgcolor="#AAAAAA">
			<th>Annotation</th>
			<th>New value</th>
		</tr>
		% for a in itemAnnotations:
			<tr>
				<th>{{a[5]}}</th>
				<th>
					% if a[3]=="LIST":	
						<select name="annotation_value_{{a[1]}}">
							% for i in listAnnotationListItems:
								% if a[4]==i[0]:
									% if a[2]==i[1]:
										<option value="{{i[1]}}" selected>{{i[1]}}</option>
									% else:
										<option value="{{i[1]}}">{{i[1]}}</option>
									% end
								% end
							% end
						</select>
					% elif a[3]=="DATE":
						<input name="annotation_value_{{a[1]}}" value="{{a[2]}}" type="date" min="2017-01-01" max="2050-01-01">
					% elif a[3]=="TEXT":
						<input type="text" size="25"  value="{{a[2]}}" name="annotation_value_{{a[1]}}">
					% else:
						Unknown type!
					{{a[1]}}
					% end
				</th>			
			</tr>
		% end
		<tr>
			<th>
				<input type="submit" name="button_annotation_modify_save" value="Save">
				<input type="reset" name="button_annotation_modify_cancel" value="Reset">
			</th>
		</tr>
	</table>

