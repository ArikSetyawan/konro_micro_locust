import time, random, uuid
from locust import HttpUser, task, between, TaskSet

class TaskFNF(TaskSet):
	@task
	def getFNFbykodekelompok(self):
		kodekelompok = random.randint(1,1000)
		self.client.get(f"/?kodekelompok={kodekelompok}")

	@task
	def getFNFbyidfnf(self):
		idfnf = random.randint(1,1000)
		self.client.get(f"/?idfnf={idfnf}")

	@task
	def postFNF(self):
		kodekelompok = random.randint(1,1000)
		tipe = random.randint(1,2)
		ranuuid = str(uuid.uuid4().hex)
		self.client.post("/",json={"kodekelompok":kodekelompok, "type":tipe, "name":ranuuid,"description":ranuuid, "backlog":ranuuid})

	@task
	def putFNF(self):
		idfnf = random.randint(1,1000)
		ranuuid = str(uuid.uuid4().hex)
		self.client.put("/",json={"idfnf":idfnf, "status":ranuuid,"description":ranuuid, "assign_to":ranuuid})

	@task
	def deleteFNF(self):
		idfnf = random.randint(1,1000)
		self.client.delete(f"/?idfnf={idfnf}")

class TaskCES(TaskSet):
	@task
	def getCESbykodekelompok(self):
		kodekelompok = random.randint(1,1000)
		self.client.get(f"/?kodekelompok={kodekelompok}")

	@task
	def getCESbyidfnf(self):
		idces = random.randint(1,1000)
		self.client.get(f"/?idces={idces}")

	@task
	def postCES(self):
		kodekelompok = random.randint(1,1000)
		tipe = random.randint(1,9)
		ranuuid = str(uuid.uuid4().hex)
		self.client.post('/', json={"kodekelompok":kodekelompok, "type":tipe, "name":"ranuuid"})

	@task
	def putCES(self):
		ranuuid = str(uuid.uuid4().hex)
		idfnf = random.randint(1,1000)
		self.client.put("/", json={"idfnf":idfnf, "name":ranuuid})

	@task
	def deleteCES(self):
		idces = random.randint(1,1000)
		self.client.get(f"/?idces={idces}")


class Taskpdc(TaskSet):
	@task
	def getpdcbykodekelompok(self):
		kodekelompok = random.randint(1,1000)
		self.client.get(f"/?kodekelompok={kodekelompok}")

	@task
	def getpdcbyidfnf(self):
		idpdc = random.randint(1,1000)
		self.client.get(f"/?idpdc={idpdc}")

	@task
	def postpdc(self):
		kodekelompok = random.randint(1,1000)
		tipe = random.randint(1,9)
		ranuuid = str(uuid.uuid4().hex)
		self.client.post('/', json={"kodekelompok":kodekelompok, "type":tipe, "name":"ranuuid"})

	@task
	def putpdc(self):
		ranuuid = str(uuid.uuid4().hex)
		idfnf = random.randint(1,1000)
		self.client.put("/", json={"idfnf":idfnf, "name":ranuuid})

	@task
	def deletepdc(self):
		idpdc= random.randint(1,1000)
		self.client.get(f"/?idpdc={idpdc}")


class Taskbmc(TaskSet):
	@task
	def getbmcbykodekelompok(self):
		kodekelompok = random.randint(1,1000)
		self.client.get(f"/?kodekelompok={kodekelompok}")

	@task
	def getbmcbyidfnf(self):
		idbmc = random.randint(1,1000)
		self.client.get(f"/?idbmc={idbmc}")

	@task
	def postbmc(self):
		kodekelompok = random.randint(1,1000)
		tipe = random.randint(1,9)
		ranuuid = str(uuid.uuid4().hex)
		self.client.post('/', json={"kodekelompok":kodekelompok, "type":tipe, "name":"ranuuid"})

	@task
	def putbmc(self):
		ranuuid = str(uuid.uuid4().hex)
		idfnf = random.randint(1,1000)
		self.client.put("/", json={"idfnf":idfnf, "name":ranuuid})

	@task
	def deletebmc(self):
		idbmc = random.randint(1,1000)
		self.client.get(f"/?idbmc={idbmc}")


class runTask(HttpUser):
	wait_time = between(5,25)
	tasks = {Taskpdc:2}