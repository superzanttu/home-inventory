%#template to show single item
<table>
	<tr bgcolor="#AAAAAA">
		<th align="left">Tavaran tunnus</th>
		<th align="left">Nimi</th>
		<th align="left">Vuosi</th>		
		<th align="left">Numero</th>
		<th align="left">Laatikko</th>		
		<th align="left">Tila</th>
		<th align="left">Muokkaa</th>
	</tr>
	<tr>
		<th align="left">{{item_id}}</th>
		<th align="left">{{item_name}}</th>
		<th align="left">{{item_year}}</th>
		<th align="left">{{item_number}}</th>
		<th align="left"><a href="/box/show/{{item_box_id}}">{{item_box_id}}</a></th>
		<th align="left">{{item_status}}</th>
		<th align="left"><a href="/item/modify/{{item_id}}">Muokkaa</a></th>
	</tr>
	<tr bgcolor="#AAAAAA">
		<th align="left" colspan="7">Kuvat</th>
	</tr>
	<tr>
		<th align="left" colspan="7">xxxx</th>
	</tr>
</table>
