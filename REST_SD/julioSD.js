const express = require("express");
const bodyParser = require("body-parser");
const julioSD = express();
const sqlite = require("sqlite3").verbose();
const url = require("url");
const { request } = require("http");
let sql;
const db = new sqlite.Database("../database.db", sqlite.OPEN_READWRITE, (err) => {
    if(err) return console.error(err);
});

julioSD.use(bodyParser.json());

// Página por defecto
julioSD.get("/",(request, response) => {
    response.json({message:'Página de inicio de aplicación de ejemplo de SD'})
    });

julioSD.post('/personaje',(req,res) => {
    console.log("Anadiendo personaje");
    try{
        ef = Math.floor((Math.random()*(10+10))-10)
        ec = Math.floor((Math.random()*(10+10))-10)
        
        const { alias, user_password } = req.body;
        sql = "INSERT INTO personaje(alias,user_password,ef,ec) VALUES (?,?,?,?)";
        db.run(sql, [ alias, user_password, ef, ec ], (err) => {
            if(err) return res.json({
                status:300,
                success: false,
                error: err
            });
            console.log("successful input ", alias, user_password);
        });
        return res.json({
            status: 200,
            success: true
        });
    } catch (error) {
        return res.json({
            status: 400, 
            success: false
        });
    };
});

julioSD.get("/personaje",(req,res)=>{
    console.log("Mostrando todos los personajes");

    sql = "SELECT * FROM personaje";
    try {
        db.all(sql,[],(err,rows)=>{
            if (err) return res.json({
                status:300,
                success: false,
                error: err
            });
            if (rows.length < 1)
                return res.json({ 
                    status: 300,
                    success: false,
                    error: "No encontrados"
                });
            return res.json({
                status: 300,
                data: rows,
                success: true
            })
        });
    } catch (error) {
        return res.json({
            status: 400,
            success: false
        });
    }
});

julioSD.get("/personaje/:id",(req,res)=>{
    console.log("Mostrando un personaje");

    const {id} = req.params;
    sql = "SELECT * FROM personaje WHERE id = ?";
    try {
        db.all(sql,[id],(err,rows)=>{
            if (err) return res.json({
                status:300,
                success: false,
                error: err
            });
            if (rows.length < 1)
                return res.json({ 
                    status: 300,
                    success: false,
                    error: "No encontrado"
                });
            if(rows.length > 1)
                return res.jso({
                    status: 300,
                    success: false,
                    error: "Demasiados resultados"
                });
            return res.json({
                status: 300,
                data: rows,
                success: true
            })
        });
    } catch (error) {
        return res.json({
            status: 400,
            success: false
        });
    }
});

julioSD.put("/personaje/:id",(req,res)=>{
    console.log("Cambiando un personaje");

    const {id} = req.params;
    const { alias, user_password } = req.body;
    sql = "UPDATE personaje SET alias = ?, user_password= ? WHERE id=?";
    try {
        db.all(sql,[alias,user_password,id],(err)=>{
            if (err) return res.json({
                status:300,
                success: false,
                error: err
            });
            return res.json({
                status: 300,
                success: true
            });
        });
    } catch (error) {
        return res.json({
            status: 400,
            success: false
        });
    };
});

julioSD.delete("/personaje/:id",(req,res)=>{
    console.log("Borrando un personaje");

    const {id} = req.params;
    sql = "DELETE FROM personaje WHERE id=?";
    try {
        db.all(sql,[id],(err)=>{
            if (err) return res.json({
                status:300,
                success: false,
                error: err
            });
            return res.json({
                status: 300,
                success: true
            });
        });
    } catch (error) {
        return res.json({
            status: 400,
            success: false
        });
    };
});

julioSD.listen(3000);