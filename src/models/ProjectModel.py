from .BaseDataModel import BaseDataModel
from .db_schemes import Project
from .enums.DataBaseEnum import DataBaseEnum

class ProjectModel(BaseDataModel):
    def __init__(self, db_client):
        super().__init__(db_client= db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECTS_NAME.value]

    async def create_project(self, project: Project):

        resault = await self.collection.insert_one(project.dict())
        project._id = resault.inserted_id
        return project

    async def get_project_or_create_one(self , project_id: str):
        record = await self.collection.find_one({"project_id": project_id})
        if record is None:
           # create new project
           project = Project(project_id=project_id)
           project = await self.create_project(project=project)
           return project

        return Project(**record)

    async def get_all_project(self, page: int =1, page_size: int =10):
        # get total size 
        total_documents = await self.collection.count_documents({})
        total_pages = (total_documents // page_size) + (1 if total_documents % page_size > 0 else 0)

        skips = page_size * (page -1)
        cursor = self.collection.find().skip(skips).limit(page_size)
        projects = []
        async for document in cursor:
            projects.append(Project(**document))
        return projects , total_pages