%#template to show all items
<table>
	<tr bgcolor="#AAAAAA">
		<th align="left">Tavaran tunnus</th>
		<th align="left">Nimi</th>
		<th align="left">Vuosi</th>
		<th align="left">Numero</th>
		<th align="left">Laatikko</th>
		<th align="left">Sijainti</th>
		<th align="left">Tila</th>
		<th align="left">Muokkaa</th></tr>
	% for i in item_list:
		<tr>
			<th align="left"><a href="/item/show/{{i[0]}}">{{i[0]}}</a></th>
			<th align="left">{{i[1]}}</th>
			<th align="left">{{i[2]}}</th>
			<th align="left">{{i[3]}}</th>
			<th align="left"><a href="/box/show/{{i[4]}}">{{i[4]}}</a></th>
			<th align="left"><a href="/location/show/{{i[5]}}">{{i[5]}}</a></th>
			% for s in status_list:
				% if i[6]==s[0]:
					<th align="left">{{s[1]}}</th>	
				% end
			% end
			
	
			<th align="left"><a href="/item/modify/{{i[0]}}">Muokkaa</a></th></tr>
	% end
</table>
