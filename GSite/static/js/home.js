get_projects = () => {
	let xhr = new XMLHttpRequest();

	let body = document.getElementById("id_content").value
	let results = document.getElementById("search_results")

	if (body) {
		let url = '/accounts/get_projects/' + body;

		xhr.open('GET', url);
		xhr.send();
		xhr.responseType = 'json';

		xhr.onload = () => {
			let projects = xhr.response['projects']
			if (projects){

				let result_content = '';

				for (let i=0; i<projects.length; i++) {

					result_content += `
						<div class="col-3 m-0 p-0 px-2">
						<ul class="list-group mb-2">
							<a style="min-height: 100px;" href="/accounts/projects/7" class="list-group-item">
								<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-journals" viewBox="0 0 16 16">
									<path d="M5 0h8a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2 2 2 0 0 1-2 2H3a2 2 0 0 1-2-2h1a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V4a1 1 0 0 0-1-1H3a1 1 0 0 0-1 1H1a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v9a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H5a1 1 0 0 0-1 1H3a2 2 0 0 1 2-2z"></path>
									<path d="M1 6v-.5a.5.5 0 0 1 1 0V6h.5a.5.5 0 0 1 0 1h-2a.5.5 0 0 1 0-1H1zm0 3v-.5a.5.5 0 0 1 1 0V9h.5a.5.5 0 0 1 0 1h-2a.5.5 0 0 1 0-1H1zm0 2.5v.5H.5a.5.5 0 0 0 0 1h2a.5.5 0 0 0 0-1H2v-.5a.5.5 0 0 0-1 0z"></path>
								</svg>
								${projects[i]["title"]}<br>

								<div class="row m-0 p-0">
									<div class="col-6 m-0 p-0">
										<span class="badge text-bg" style="background-color: ${projects[i]['color']}; color: ${projects[i]['color']};">-</span>
										${projects[i]["category"]}
									</div>
									<div class="col-6 m-0 p-0">
										<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#FFD700" class="bi bi-star-fill" viewBox="0 0 16 16">
										  <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"></path>
										</svg>
										${projects[i]["likes"]}
									</div>
								</div>

								<div class="row m-0 p-0">
									<span class="col-12 m-0 p-0">Автор: ${projects[i]["user"]["username"]}</span>
								</div>
							</a>
						</ul>
					</div>
					`
				}
				results.innerHTML = result_content;
				$('#search_results').show();
			} else {
				$('#search_results').hide();
			}
		}
	} else {
		$('#search_results').hide();
	}

}

generate_chart = () => {
	const ctx = document.getElementById('myChart');


	let xhr = new XMLHttpRequest();
	xhr.open('GET', '/accounts/get_diagram_data');
	xhr.send();
	xhr.responseType = 'json';

	xhr.onload = () => {

		let labels_ = [];
		let keys = [];
		let colors = [];

		Object.entries(xhr.response).forEach(([key, value]) => {
		   labels_.push(key)
		   keys.push(value['count'])
		   colors.push(value['color'])
		});

		const data = {
		  labels: labels_,
		  datasets: [{
		    data: keys,
		    backgroundColor: colors,
		    hoverOffset: 4
		  }]
		};

		new Chart(ctx, {
		type: 'doughnut',
		data: data,
		options: {
			scales: {
				y: {
					beginAtZero: true
				}
			}
		}
	});

	}
}

generate_chart()
