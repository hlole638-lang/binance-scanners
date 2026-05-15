async function scan() {

    const tf = document.getElementById("timeframe").value

    const res = await fetch(`/scan/${tf}`)

    const data = await res.json()

    const tbody = document.getElementById("results")

    tbody.innerHTML = ""

    data.forEach(c => {

        tbody.innerHTML += `
        <tr>
            <td>${c.symbol}</td>
            <td>${c.price}</td>
            <td>${c.rsi}</td>
            <td>${c.score}</td>
        </tr>
        `
    })

    notify()
}

function notify() {

    if (Notification.permission === "granted") {

        new Notification("تم العثور على فرص جديدة")
    }
}

Notification.requestPermission()
