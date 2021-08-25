%#template to show location info and list of all boxes
<table>
	<tr bgcolor="#AAAAAA">
		<th align="left">Sijainnin tunnus</th>
		<th align="left">Nimi</th>
		<th align="left">Tila</th>
		<th align="left">Muokkaa</th>
	</tr>
	<tr>
		<th align="left">{{location_id}}</th>
		<th align="left">{{location_name}}</th>
		<th align="left">{{location_status}}</th>
		<th align="left"><a href="/location/modify/{{location_id}}">Muokkaa</a></th>
	</tr>
</table>

<table>
	<tr bgcolor="#AAAAAA">
		<th align="left">Tunnus</th>
		<th align="left">Nimi</th>
		<th align="left">Sijainti</th>
		<th align="left">Täyttöaste</th>
		<th align="left">Tila</th>
		<th align="left">Muokkaa</th>
	</tr>
	
	% for b in location_box_list:
		<tr>
			<th align="left"><a href="/box/show/{{b['id']}}">{{b['id']}}</a></th>
			<th align="left">{{b['name']}}</th>
			<th align="left"><a href="/location/show/{{b['location_id']}}">{{b['location_id']}}</th>
			<th align="left">{{b['occupancy']}}</th>
			<th align="left">{{b['status']}}</th>
			<th align="left"><a href="/box/modify/{{b['id']}}">Muokkaa</a></th>
		</tr>
	% end
	
</table>
