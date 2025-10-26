from gmpy2 import gcd
from Crypto.Util.number import long_to_bytes

N = 53631231719770388398296099992823384509917463282369573510894245774887056120440201731735752915096736722856082884548917654078388282501542293219713052500317361
g1 = 27888419610931008932601664194635863362934795268815711191831564335481311281875775885782976960387128801701810764586184606874328259752328953489610371824189861
g2 = 48099264739307394087061906063506998841178675587231635606136922987485103900358857801144199074460106065443613588490877251721439499846448566220473205526148817

p = gcd(g1-1,N)
q = gcd(g2-1,N)

cs =[]
with open("WIM.mp4.cipher", "rb") as f:
    lines = [line.strip() for line in f if line.strip()]
for i in range(0, len(lines), 2):
    c1 = int(lines[i])
    c2 = int(lines[i+1])
    cs.append((c1, c2))

def crt(m_p, m_q, p, q):
    inv_p_mod_q = pow(p, -1, q)
    t = ((m_q - m_p) * inv_p_mod_q) % q
    return (m_p + p * t) % (p * q)

Seq = bytearray()
for c1,c2 in cs:
    mp = c1 %p
    mq = c2 %q
    m = (mp + p * (((mq - mp) * pow(p,-1,q)) % q))
    Seq += m.to_bytes(64,"big")
Seq = bytes(Seq)

l = len(Seq)
while Seq[l-1] == 114:
    l -= 1
    if l == 0:
        break
Seq = Seq[:l]
blob = Seq[:-3]
open("WIM.mp4","wb").write(blob)
