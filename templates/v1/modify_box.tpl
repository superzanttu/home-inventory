%#template for location modify box
<form action="/box/modify/{{box_id}}" method="POST" enctype="multipart/form-data">
	<table>
		<tr bgcolor="#AAAAAA">
			<th>Laatikon tunnus</th>
			<th>Nimi</th>
			<th>Sijainti</th>
			<th>Täyttöaste</th>
			<th>Tila</th>
		</tr>
		<tr>
			<th><input type="text" name="id" value="{{box_id}}"></th>
			<th><input type="text" name="name" value="{{box_name}}"></th>

			<th><select name="location">
					% for s in box_location_list:
						% if s==box_location_id:
							<option selected value={{s}}>{{s}}</option>
						% else:
							<option value={{s}}>{{s}}</option>
						% end
						
					% end
				</select>
			</th>

			<th><input type="text" name="occupancy" value="{{box_occupancy}}"></th>
			
			<th><select name="status">
					% for s in box_status_list:
						% if s[0]==box_status_id:
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