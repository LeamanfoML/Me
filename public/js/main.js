const REFRESH_INTERVAL = 10000;
let timerId;

async function fetchData() {
  const minProfit = document.getElementById('minProfit').value;
  const sortBy = document.getElementById('sortBy').value;
  const url = `/api/data?minProfit=${minProfit}&sortBy=${sortBy}`;
  const res = await fetch(url);
  const data = await res.json();
  const tbody = document.querySelector('#tbl tbody');
  tbody.innerHTML = '';
  data.forEach(item => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${item.name}</td>
      <td>${item.model}</td>
      <td>${new Date(item.ends_at).toLocaleString()}</td>
      <td>${item.current_bid.toFixed(3)}</td>
      <td>${item.portals_price.toFixed(3)}</td>
      <td>${item.tonnel_price.toFixed(3)}</td>
      <td>${item.profit.toFixed(3)}</td>
    `;
    tbody.append(tr);
  });
}

function schedule() {
  clearInterval(timerId);
  timerId = setInterval(() => {
    document.getElementById('refresh').click();
  }, REFRESH_INTERVAL);
}

document.getElementById('refresh').addEventListener('click', async () => {
  await fetch('/api/update', { method: 'POST' });
  await fetchData();
});

document.getElementById('minProfit').addEventListener('change', fetchData);
document.getElementById('sortBy').addEventListener('change', fetchData);

window.onload = () => {
  document.getElementById('refresh').click();
  schedule();
};
