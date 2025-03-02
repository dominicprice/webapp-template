import { FormEvent, useEffect, useRef, useState } from "react";
import { getPings, ping, PingResponse } from "./lib/client";
import PingTable from "@/components/pingtable";

interface FormElements extends HTMLFormControlsCollection {
	dataInput: HTMLInputElement;
}

interface PingFormElement extends HTMLFormElement {
	readonly elements: FormElements;
}

const App = () => {
	const input = useRef<HTMLInputElement | null>(null);
	const [pings, setPings] = useState<PingResponse[]>([]);
	useEffect(() => {
		getPings({
			query: {
				sort_direction: "desc",
			},
		}).then((resp) => setPings(resp.data?.results ?? []));
	}, []);
	const onPing = (e: FormEvent<PingFormElement>) => {
		e.preventDefault();
		const data = e.currentTarget.elements.dataInput.value;
		ping({ body: { data: data } })
			.then((resp) => {
				if (resp.data) {
					setPings((prev) => [resp.data, ...prev]);
				}
			})
			.then(() => {
				const elem = input.current;
				if (!elem) return;
				elem.value = "";
			});
	};

	return (
		<div className="flex flex-col gap-2 items-center m-4">
			<form className="flex flex-row gap-2 p-4" onSubmit={onPing}>
				<input
					ref={input}
					className="border rounded shadow p-2 outline-none"
					id="dataInput"
				/>
				<button className="rounded shadow p-2 bg-sky-300" type="submit">
					Ping!
				</button>
			</form>
			<PingTable pings={pings} />
		</div>
	);
};

export default App;
