%#template to show all boxes
<table>
	<tr bgcolor="#AAAAAA">
		<th align="left">Laatikon tunnus</th>
		<th align="left">Nimi</th>
		<th align="left">Sijainti</th>		
		<th align="left">Täyttöaste</th>		
		<th align="left">Tila</th>
		<th align="left">Muokkaa</th>
	</tr>
	<tr>
		<th align="left">{{box_id}}</th>
		<th align="left">{{box_name}}</th>
		<th align="left"><a href="/location/show/{{box_location_id}}">{{box_location_id}}</a></th>
		<th align="left">{{box_occupancy}}</th>
		<th align="left">{{box_status}}</th>
		<th align="left"><a href="/box/modify/{{box_id}}">Muokkaa</a></th>
	</tr>
</table>

<table>
	<tr bgcolor="#AAAAAA">
		<th align="left">Tunnus</th>
		<th align="left">Nimi</th>
		<th align="left">Vuosi</th>		
		<th align="left">Numero</th>		
		<th align="left">Laatikko</th>
		<th align="left">Tila</th>
		<th align="left">Muokkaa</th>
	</tr>
	% for i in box_item_list:
		<tr>
			<th align="left"><a href="/item/show/{{i['id']}}">{{i['id']}}</a></th>
			<th align="left">{{i['name']}}</th>
			<th align="left">{{i['year']}}</th>
			<th align="left">{{i['number']}}</th>
			<th align="left"><a href="/box/show/{{i['box_id']}}">{{i['box_id']}}</a></th>
			<th align="left">{{i['status']}}</th>
			<th align="left"><a href="/item/modify/{{i['id']}}">Muokkaa</a></th>
		</tr>
	% end
</table>