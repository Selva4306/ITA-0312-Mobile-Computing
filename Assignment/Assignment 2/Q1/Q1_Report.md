# Assignment 2 – Q1: Mobile Communication or Mobile Computing?

**Field-Service Technology Audit | 5 Marks**

## 1. Definitions and classification criteria

**Wireless** means that a communication link uses radio or another non-cabled medium. **Mobile** means that a user or device can change physical location while carrying out a task or maintaining a service. **Nomadic** means the device is moved between locations but is generally used while stationary at each location. **Mobile communication** concerns connectivity and information exchange during movement; **mobile computing** also includes application, data and service behaviour under mobility and intermittent connectivity.

Classification criteria:

1. **User mobility:** Can the worker/device move while remaining in use, or is it installed at one site?
2. **Access medium:** Is the data path wired, wireless or mixed?
3. **Disconnection tolerance:** Can work continue offline and synchronise later, or must the link be continuously available?
4. **Context awareness:** Does the application use location, time, asset identity or local context?
5. **Resource and interaction constraints:** Are there power, ruggedness, small-screen or real-time voice requirements?

## 2. Predictions for the five cases

| Case | Classification | Main problem area | Reason |
|---|---|---|---|
| (a) Rugged tablet fetching work orders over cellular | **Mobile** | Mainly mobile computing, supported by mobile communication | Worker carries it between job sites; cellular is wireless. Work-order retrieval, local task state and reconnection behaviour are application concerns. |
| (b) Laptop plugged into Ethernet at different offices | **Nomadic** | Conventional computing/network access; not inherently mobile communication | It is relocated between offices but used at a fixed desk and wired at each stop. Mobility is intermittent rather than continuous. |
| (c) Fixed wireless router at remote substation | **Fixed-wireless** | Mainly fixed wireless communication | The router is stationary; the radio link replaces a cable. Wireless does not make the endpoint mobile. |
| (d) Push-to-talk handset | **Mobile** | Mainly mobile communication | A portable handset supports real-time voice while staff move. The dominant requirement is low-latency, reliable communication. |
| (e) Tablet records meter readings offline and synchronises later | **Mobile** | Mainly mobile computing, with deferred mobile communication | The app must store data safely, timestamp and identify readings, resolve retries/duplicates, and synchronise when coverage returns. |

## 3. Additional ambiguous case

A technician carries a rugged laptop between substations, but it is used only when docked to a fixed wired LAN at each site. The hardware is portable, but the work pattern is stationary-at-a-time and wired. Under the criteria it is **nomadic**, rather than fully mobile. It becomes a mobile-computing problem if the application must support work during movement, offline field tasks or location-aware services.

## 4. Simulation design

The simulation models case (e), not radio performance in detail.

- A six-hour shift contains **60 meter updates**, generated every six minutes.
- Each minute independently has a working link with probability **90%, 60% or 30%**.
- **Send immediately:** each update is attempted only at its creation minute. If disconnected at that minute, the update is lost.
- **Store-and-forward:** updates enter a FIFO queue with capacity 12. During each connected minute, one queued update is transmitted. If the queue is full, the newest update is dropped.
- The run ends after 360 minutes. Items still queued are reported as **pending**, not lost.
- A fixed random seed and **5,000 trials** are used. Values below are averages per 60 generated updates, so fractional counts are expected values.

Delay is measured from update creation to successful transmission. An update sent immediately in its creation minute has zero delay.

## 5. Simulation results

| Link availability | Immediate delivered | Immediate delayed | Immediate lost | Store-forward delivered | Store-forward delayed deliveries | Store-forward lost | Pending at shift end | Store-forward mean delay |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 90% | 54.04 | 0.00 | 5.96 | 60.00 | 5.96 | 0.00 | 0.00 | 0.11 min |
| 60% | 36.02 | 0.00 | 23.98 | 60.00 | 24.12 | 0.00 | 0.00 | 0.67 min |
| 30% | 17.94 | 0.00 | 42.06 | 59.77 | 45.03 | 0.00 | 0.23 | 3.03 min |

The counts are averages across 5,000 runs; the store-and-forward results at 60% and 30% may therefore be fractional. No queue overflow occurred on average in these runs. The small number still pending at the end of the 30% case is not counted as delivered or lost.

## 6. Inquiry and interpretation

The results show that a wireless link alone does not provide continuity. Mobile computing needs local persistence, buffering, retry logic, ordering, timestamps, duplicate protection, conflict handling and clear feedback about pending synchronisation.

At 30% availability, store-and-forward delivers about **59.77 of 60** updates on average, while immediate sending delivers about **17.94**. The improvement comes with additional delay: the mean delay among successfully delivered queued updates is about **3.03 minutes**.

The tablet in case (e) definitely needs application-level offline-first changes. Case (a) also benefits from cached work orders and resumable requests. The push-to-talk handset needs communication-layer handover and reliability rather than an offline data queue. The fixed router and Ethernet laptop do not become mobile-computing systems merely because one uses radio or the other is portable.

## 7. Conclusion

Wireless and mobile are not synonyms. Wireless identifies the transmission medium; mobile identifies a mobility pattern. Mobile communication focuses on moving information between endpoints while users/devices move. Mobile computing additionally concerns the applications, data and services that must remain useful despite movement, variable connectivity, limited resources and changing context.

Therefore, case (c) is wireless but fixed, case (b) is portable/nomadic but wired, and case (e) exposes the defining application challenges of mobile computing.

## Reproducibility

Install dependencies with `pip install -r requirements.txt`, then run `python q1.py` from this folder. The fixed seed regenerates `data/simulation_results.csv`.
