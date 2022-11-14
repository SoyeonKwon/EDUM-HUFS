from channels.generic.websocket import AsyncJsonWebsocketConsumer


class CamConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("cameras", self.channel_name)
        print(f"Added {self.channel_name} channel to cameras")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("cameras", self.channel_name)
        print(f"Removed {self.channel_name} channel to cameras")

    async def cam_message(self, event):
        await self.send_json(event)
        print(f"Got message {event} at {self.channel_name}")
