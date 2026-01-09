- clean le snap
# snapcraft clean
- build le snap
# snapcraft pack

- verifier si snap est installer 
# snap list | grep lmrtask

- desinstaller 
# sudo snap remove lmrtask

- installer en mode dev
# sudo snap install lmrtask_1.0_amd64.snap --dangerous
- desinstaller avec dev
# sudo snap remove lmrtask --purge


