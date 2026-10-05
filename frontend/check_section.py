from pathlib import Path

file = Path("src/pages/Dashboard.jsx")
content = file.read_text(encoding="utf-8")

start = content.index('<div className="card">', content.index('<h2>Your Skills</h2>') - 100)
end = content.index('</div>', content.index('onClick={() => predictCareer()}')) + len('</div>')

print("Skill section boundaries found")
print("Start:", start)
print("End:", end)
