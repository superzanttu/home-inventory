% # Modify container attributes
% cTypes = [["BUILDING","Building"],["ROOM","Room"],["SHELVES","Shelves"],["SHELF","Shelf"],["BOX","Box"]]
<form action="/modify/container_attributes/{{modifyContainerID}}" method="POST" enctype="multipart/form-data">
	<table>
		<tr bgcolor="#AAAAAA"><th>Container ID</th><th style="max-width:10%;">Container Container ID</th><th>Container Type</th><th>Container Name</th></tr>
		<tr>
			<th><input type="text" name="new_container_id" value="{{modifyContainerID}}"></th>
			<th><select name="new_container_container_id" value="0">
					% for c in listContainers:
						% if c != modifyContainerID:
							% if c[0]==modifyContainerContainerID:
								<option selected value={{c[0]}}>{{c[1]}}</option>
							% else:
								<option value={{c[0]}}>{{c[1]}}</option>
							% end
						% end
					% end
				</select>
			</th>

			<th><select name="new_container_type" value="0">
					% for c in cTypes:
						% if c[0]==modifyContainerType:
							<option selected value={{c[0]}}>{{c[1]}}</option>
						% else:
							<option value={{c[0]}}>{{c[1]}}</option>
						% end
					% end
				</select>
			</th>
			<th><input type="text" name="new_container_name" value="{{modifyContainerName}}"></th>
			
		</tr>
		
		<tr>
			<th>
				<input type="submit" name="button_modify_container_attributes" value="Save changes">
				<input type="reset" name="button_reset_item_attributes" value="Reset values">
			</th>
		</tr>
	</table>
</form>