import { PingResponse } from "@/lib/client";

interface PingTableProps {
	pings: PingResponse[];
}
const PingTable = ({ pings }: PingTableProps) => {
	return (
		<table>
			<thead>
				<tr className="bg-sky-100">
					<th className="p-2">Timestamp</th>
					<th className="p-2">Data</th>
				</tr>
			</thead>
			<tbody>
				{pings.map((p) => (
					<tr className="odd:bg-neutral-50" key={p.id}>
						<td className="p-2">{p.timestamp}</td>
						<td className="p-2">{p.data}</td>
					</tr>
				))}
			</tbody>
		</table>
	);
};

export default PingTable;
