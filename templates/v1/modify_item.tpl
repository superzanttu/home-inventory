%#template for location modify item
<form action="/item/modify/{{item_id}}" method="POST" enctype="multipart/form-data">
	<table>
		<tr bgcolor="#AAAAAA">
			<th>Tavaran tunnus</th>
			<th>Nimi</th>
			<th>Laatikko</th>
			<th>Tila</th>
			<th>Kuvat</th>
		</tr>
		<tr>
			<th><input type="text" name="id" value="{{item_id}}" readonly></th>
			<th><input type="text" name="name" value="{{item_name}}"></th>

			<th><select name="box_id">
					% for s in item_box_list:
						% if s==item_box_id:
							<option selected value={{s}}>{{s}}</option>
						% else:
							<option value={{s}}>{{s}}</option>
						% end
						
					% end
				</select>
			</th>
			
			<th><select name="status">
					% for s in item_status_list:
						% if s[0]==item_status_id:
							<option selected value={{s[0]}}>{{s[1]}}</option>
						% else:
							<option value={{s[0]}}>{{s[1]}}</option>
						% end
						
					% end
				</select>
			</th>
		</tr>

		<tr>
			<th><input type="submit" name="save" value="Tallenna"></th>
		</tr>
  	</table>
</form>

			<form action="/item/upload_picture/{{item_id}}" method="POST" enctype="multipart/form-data">
  			<input type="file" name="item_picture" />
  			%#<input type="text" name="id" value="{{item_id}}">
  			<input type="submit" value="Save" />
			</form>