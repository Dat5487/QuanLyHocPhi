from app.models import *
import time
import hashlib
from datetime import datetime
from django.shortcuts import render

class Blockchain:
    def add_block(self, maSinhVien, maThanhToan, soTien, noiDung, soGiaoDich, ketQua):
        if BlockChain.objects.exists():
            previous_block = self.get_latest_block()
            index = previous_block.index + 1
            previous_hash = previous_block.hash
        else:
            index = 0
            previous_hash = ""
        timestamp = datetime.now()
        nonce = self.calculate_nonce(index, timestamp, maSinhVien, maThanhToan,
                                     soTien, noiDung, soGiaoDich, ketQua, previous_hash)
        
        hash = self.calculate_hash(index, timestamp, maSinhVien, maThanhToan,
                                    soTien, noiDung, soGiaoDich, ketQua, previous_hash, nonce)
        
        block = BlockChain(index=index, timestamp=timestamp, maSinhVien=maSinhVien,
                       maThanhToan=maThanhToan, soTien=soTien, noiDung=noiDung,
                         soGiaoDich=soGiaoDich, ketQua=ketQua, previous_hash=previous_hash, hash=hash ,nonce=nonce)
        block.save()
        return
        
    def is_valid_block(self, block, previous_block):
        if block.index != previous_block.index + 1:
            return False
        if block.previous_hash != previous_block.hash:
            return False
        if block.hash != self.calculate_hash(block.index, block.timestamp, block.maSinhVien,block.maThanhToan, block.soTien, block.noiDung, block.soGiaoDich, block.ketQua, block.previous_hash, block.nonce):
            return False
        return True


    def is_valid_chain(self):
        invalid_blocks = []
        blocks = BlockChain.objects.order_by('index')
        previous_block = blocks[0]
        for block in blocks[1:]:
            if not self.is_valid_block(block, previous_block):
                invalid_blocks.append(block)
            previous_block = block
        return invalid_blocks
    
    def get_latest_block(self):
        return BlockChain.objects.latest('index')


    def calculate_hash(self, index, timestamp, maSinhVien, maThanhToan, soTien, noiDung, soGiaoDich, ketQua, previous_hash, nonce):
        sha = hashlib.sha256()
        sha.update(str(index).encode('utf-8') +
                   str(timestamp).encode('utf-8') +
                   str(maSinhVien).encode('utf-8') +
                   str(maThanhToan).encode('utf-8') +
                   str(soTien).encode('utf-8') +
                   str(noiDung).encode('utf-8') +
                   str(soGiaoDich).encode('utf-8') +
                   str(ketQua).encode('utf-8') +
                   str(previous_hash).encode('utf-8') +
                   str(nonce).encode('utf-8'))
        return sha.hexdigest()
    
    def calculate_nonce(self, index, timestamp, maSinhVien, maThanhToan, soTien, noiDung, soGiaoDich, ketQua,
                        previous_hash):
        nonce = 0
        while True:
            nonce_str = str(nonce)
            hash = self.calculate_hash(index, timestamp, maSinhVien, maThanhToan, soTien, noiDung, soGiaoDich, ketQua,
                                       previous_hash, nonce_str)
            if hash.startswith('00'):  # Adjust the required number of leading zeroes as per your needs
                return nonce_str
            nonce += 1
            time.sleep(0.01)  # Add a small delay to avoid excessive CPU usage

def add_block(request):
    blockchain = Blockchain()
    maSinhVien = "1"  
    maThanhToan = "1"  
    soTien = "1"  
    noiDung = "1"  
    soGiaoDich = "1"  
    ketQua = "1"  
    blockchain.add_block(maSinhVien, maThanhToan, soTien, noiDung, soGiaoDich, ketQua)
    return render(request, 'success.html')

